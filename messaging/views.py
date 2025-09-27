# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError, transaction
from products.models import Product
from .models import Thread, Message
from .forms import MessageForm

@login_required
def inbox(request):
    threads = Thread.objects.filter(buyer=request.user) | Thread.objects.filter(seller=request.user)
    threads = threads.order_by("-last_message_at", "-updated_at").select_related("product", "buyer", "seller")
    # simple unread count per thread
    unread_counts = {
        t.id: Message.objects.filter(thread=t, recipient=request.user, is_read=False).count()
        for t in threads
    }
    return render(request, "messaging/inbox.html", {"threads": threads, "unread_counts": unread_counts})

@login_required
def start_thread(request, product_id):
    """Buyer clicks 'Message Seller' from a product page."""
    product = get_object_or_404(Product, pk=product_id)
    seller = product.seller
    buyer = request.user

    if buyer == seller:
        messages.info(request, "You are the seller of this item.")
        return redirect("products:product_detail", product_id=product.id) if "products" in request.resolver_match.namespace else redirect("product_detail", product_id=product.id)

    try:
        with transaction.atomic():
            thread, created = Thread.objects.get_or_create(
                product=product, seller=seller, buyer=buyer
            )
    except IntegrityError:
        thread = Thread.objects.get(product=product, seller=seller, buyer=buyer)

    return redirect("messaging:thread_detail", pk=thread.id)

@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    # permission: only buyer or seller can view
    if request.user not in (thread.buyer, thread.seller):
        messages.error(request, "You don't have access to this conversation.")
        return redirect("messaging:inbox")

    # mark incoming messages as read
    Message.objects.filter(thread=thread, recipient=request.user, is_read=False).update(is_read=True)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.thread = thread
            msg.sender = request.user
            msg.recipient = thread.other_user(request.user)
            msg.save()
            send_email = msg.recipient.email
            if send_email:
                # Send email notification logic here
                
                subject = f"New message about {thread.product.product_name}"
                message = f"You have a new message from {msg.sender} regarding the product '{thread.product.product_name}'.\n\nMessage:\n{msg.body}\n\nView the conversation: http://{request.get_host()}/messages/thread/{thread.id}/"
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [send_email])

            return redirect("messaging:thread_detail", pk=thread.id)
    else:
        form = MessageForm()

    msgs = thread.messages.select_related("sender", "recipient")
    return render(request, "messaging/thread_detail.html", {"thread": thread, "messages": msgs, "form": form})

