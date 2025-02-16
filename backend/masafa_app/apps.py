from django.apps import AppConfig


class MasafaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'masafa_app'

    def ready(self):
        import core.signals
        import masafa_app.signals