from django.db import models
from .utils import send_telegram_message

dialogue_statuses = (
    (0, 'Неактивен'),
    (1, 'Активен')
)


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=30, verbose_name='Имя')
    phone = models.CharField(
        max_length=15, verbose_name='Телефон', null=True, blank=True)
    age_confirmed = models.BooleanField(
        default=False, verbose_name='Подтверждение возраста')
    phone_confirmed = models.BooleanField(
        default=False, verbose_name='Подтверждение телефона')
    sf_member = models.BooleanField(
        default=False, verbose_name='Участник программы лояльности')
    state = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'Пользователь {}'.format(self.name)

    def __init__(self, *args, **kwargs):
        super(BotUser, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id:
            previous = BotUser.objects.get(id=self.id)
            if not previous.sf_member and self.sf_member:
                resp = send_telegram_message(
                    self.telegram_id, 'Мы проверили, вы являетесь учаcтником программы лояльности', next_state=True)
                if resp['ok'] and resp.get('data'):
                    # delete field sf_member to avoid replace
                    resp['data'].pop('sf_member')
                    for name, value in resp['data'].items():
                        object.__setattr__(self, name, value)
        super(BotUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class SmsCode(models.Model):
    user = models.ForeignKey(
        BotUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    code = models.IntegerField(verbose_name='Код')

    class Meta:
        verbose_name = 'Смс код'
        verbose_name_plural = 'Смс коды'


class Dialogue(models.Model):
    user = models.ForeignKey(
        BotUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.IntegerField(default=1, choices=dialogue_statuses)

    def __str__(self):
        return 'Диалог c {}'.format(self.user.name)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'


class DialogueMessage(models.Model):
    dialogue = models.ForeignKey(
        Dialogue, on_delete=models.CASCADE, verbose_name='Диалог', related_name='messages')
    message = models.TextField(verbose_name='Сообщение')
    from_user = models.BooleanField()

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
