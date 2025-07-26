from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .fcm import send_push_notification

class SendPushView(APIView):
    def post(self, request):
        token = request.data.get("token")
        title = request.data.get("title")
        body = request.data.get("body")
        mytype = request.data.get("mytype")
        mytypeid = request.data.get("mytypeid")
     

        if not all([token, title, body]):
            return Response({"error": "token, title и body обязательны!"}, status=400)

        code, result = send_push_notification(token, title, body, mytype, mytypeid)
        return Response({"status_code": code, "result": result})
