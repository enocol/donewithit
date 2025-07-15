from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

def ready(self):
        import checkout.signals  # Import signals to ensure they are registered
        # This will ensure that the signals are connected when the app is ready
        # and will handle post_save and post_delete events for OrderItem model.