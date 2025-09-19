from django.shortcuts import render

# Create your views here.

# newsletter/views.py
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings

from .forms import NewsletterSignupForm
from .models import Subscriber

def signup(request):
    ''' Display the newsletter signup form '''
    form = NewsletterSignupForm()
    context = {"form": form}
    return render(request, "subscriptions/signup.html", context)

def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if the email already exists
            if Subscriber.objects.filter(email=email).exists():
                messages.info(request, "You are already subscribed to the newsletter.")
            else:
                # Save the new subscriber
                form.save()
                # Send a welcome email
                send_mail(
                    "Welcome to Our Newsletter",
                    "Thank you for subscribing to our newsletter!",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect(reverse("home"))
    else:
        form = NewsletterSignupForm()

    return render(request, "subscriptions/signup.html", {"form": form})
