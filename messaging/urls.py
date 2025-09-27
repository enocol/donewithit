from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("thread/<int:pk>/", views.thread_detail, name="thread_detail"),
    path("start/<int:product_id>/", views.start_thread, name="start_thread"),
]
