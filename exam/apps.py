from django.apps import AppConfig


class examConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exam'


    def ready(self):
        import exam.models 