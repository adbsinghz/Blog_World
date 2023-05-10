from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals 
'''from django.contrib.auth.models import User
from users.models import Profile
user = User.objects.get(username='arsh')
profile = Profile(user=user)
profile.save()'''