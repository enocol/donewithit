# newsletter/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("newsletter-signup/", views.newsletter_signup, name="newsletter_signup"),
]
