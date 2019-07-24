from rest_framework import serializers
from . import models


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BotUser
        fields = '__all__'


class SmsCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SmsCode
        fields = '__all__'


class DialogueSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.DialogueMessage.objects.all())
    user = serializers.IntegerField(source='user.telegram_id')

    def create(self, validated_data):
        user = validated_data.get('user')
        user = models.BotUser.objects.filter(
            telegram_id=user['telegram_id']).first()
        if not user:
            raise 'User not found'
        validated_data['user'] = user
        return super(DialogueSerializer, self).create(validated_data)

    class Meta:
        model = models.Dialogue
        fields = '__all__'


class DialogueMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DialogueMessage
        fields = '__all__'
