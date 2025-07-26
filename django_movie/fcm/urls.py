from django.urls import path
from .views import SendPushView

urlpatterns = [
    path("send-push/", SendPushView.as_view(), name="send_push"),
]
