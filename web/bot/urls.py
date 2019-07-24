from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.BotUserViewSet)
router.register(r'dialogues', views.DialogueViewSet)
router.register(r'messages', views.DialogueMessageViewSet)

urlpatterns = [
    path('sendSmsCode', views.send_sms_code_view),
    path('acceptSmsCode', views.accept_sms_code_view),
    path('', include(router.urls))
]
