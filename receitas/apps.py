from django.apps import AppConfig
from django.apps import AppConfig


class ReceitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receitas'
    def ready(self):
        from django.contrib.auth.models import User

        def __create_default_user():
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                print('Usuário admin criado com sucesso!')
