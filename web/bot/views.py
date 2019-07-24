from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models, serializers, utils


class BotUserViewSet(viewsets.ModelViewSet):
    queryset = models.BotUser.objects.all()
    serializer_class = serializers.BotUserSerializer
    lookup_field = 'telegram_id'


class DialogueViewSet(viewsets.ModelViewSet):
    queryset = models.Dialogue.objects.all()
    serializer_class = serializers.DialogueSerializer
    lookup_field = 'user__telegram_id'


class DialogueMessageViewSet(viewsets.ModelViewSet):
    queryset = models.DialogueMessage.objects.all()
    serializer_class = serializers.DialogueMessageSerializer


@api_view(['GET'])
def send_sms_code_view(request):
    if request.GET.get('user_id'):
        user = models.BotUser.objects.filter(
            telegram_id=request.GET.get('user_id')).first()
        if user:
            code = utils.generate_sms_code()
            models.SmsCode.objects.create(user=user, code=code)
            utils.send_sms(user.phone, code)
            return Response({'ok': True}, status=200)
        return Response({'ok': False, 'message': 'user not found'}, status=404)
    return Response({'ok': False, 'message': 'missing parameter'}, status=400)


@api_view(['GET'])
def accept_sms_code_view(request):
    if request.GET.get('user_id') and request.GET.get('code'):
        note = models.SmsCode.objects.filter(
            user_id=request.GET.get('user_id')).order_by('-id').first()
        if note:
            if str(note.code) == request.GET.get('code'):
                note.user.phone_confirmed = True
                note.save()
                return Response({'ok': True})
            return Response({'ok': False, 'message': 'wrong code'}, status=200)
        return Response({'ok': False, 'message': 'user not found'}, status=404)
    return Response({'ok': False, 'message': 'missing parameter'}, status=400)
