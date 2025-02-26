from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'  # The name of the app
    verbose_name = 'Core Application'

    def ready(self):
        # Import signals to ensure they are connected to pre_save across all apps
        import core.signals  # Ensure signals are loaded for the whole project
