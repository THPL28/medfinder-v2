from django.core.mail import send_mail
from django.conf import settings

def enviar_email(destinatario, assunto, mensagem, remetente=None):
    remetente = remetente or settings.DEFAULT_FROM_EMAIL
    send_mail(
        assunto,
        mensagem,
        remetente,
        [destinatario],
        fail_silently=False,
    )
