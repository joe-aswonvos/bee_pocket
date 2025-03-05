from django.apps import AppConfig


class PocketAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pocket_app'
    
    def ready(self):
        import pocket_app.signals
