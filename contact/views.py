# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.user, request.POST)
        if contact_form.is_valid():
            message = contact_form.save()
            messages.success(request, "Thanks! Your message has been sent.")

            
            to_address = getattr(settings, "CONTACT_RECIPIENT_EMAIL", None)
            if to_address:
                subject = message.subject or "New contact message"
                body = (
                    f"From: {message.name} <{message.email}>\n"
                    f"User ID: {message.user_id or 'guest'}\n\n"
                    f"{message.message}"
                )
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to_address], fail_silently=True)

            messages.info(request, "You will receive a reply to your email address if necessary.")
            return redirect("profile")  
    else:
        contact_form = ContactForm(request.user)

    return render(request, "contact/contact.html", {"form": contact_form})

