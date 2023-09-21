"""registering the app core for django"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """core configuration for the core app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """signal to create user profile while creating user"""
        import core.signals
