from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .utils import send_telegram_message
from . import models


@receiver(pre_save, sender=models.DialogueMessage)
def message_sender(sender, instance, *args, **kwargs):
    if not instance.id and not instance.from_user:
        send_telegram_message(
            instance.dialogue.user.telegram_id, instance.message)
