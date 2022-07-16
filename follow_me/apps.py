from django.apps import AppConfig


class FollowMeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'follow_me'
    
    # def ready(self):
    #     import follow_me.signals
