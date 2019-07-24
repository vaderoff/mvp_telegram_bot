from django.contrib import admin
from . import models


@admin.register(models.BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telegram_id', 'phone', 'sf_member')
    readonly_fields = ('id', 'state')


@admin.register(models.SmsCode)
class SmsCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code')


@admin.register(models.Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')


@admin.register(models.DialogueMessage)
class DialogueMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'dialogue', 'message', 'from_user')
