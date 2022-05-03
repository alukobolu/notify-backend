from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from rest_framework.permissions import AllowAny,IsAuthenticated
from accounts.models import User, UserAccount
from notifications.utils import send_push_message
from .models import Notification_table
from rest_framework.pagination import PageNumberPagination
# Create your views here.


paginator = PageNumberPagination()
paginator.page_size = 6


class NotifyMe(APIView):
    permission_classes = [IsAuthenticated]

    def final_push(self,user_account, title, message,sender):
        token = user_account.expo_push_token
        try : 
            note = Notification_table()
            note.recieve_user = user_account
            note.send_user = sender
            note.title = title
            note.message = message
            note.save()
            send_push_message(token, title, message)
        except : 
            pass  

    def send_notification(self,users, title, message,sender) :
        if users == "ALL":
            user_accounts = UserAccount.objects.all()
            for user in user_accounts:
                self.final_push(user,title,message,sender)
        else:
            emails = users.split(",")
            for email in emails:
                user = User.objects.get(email = email)
                user_account = UserAccount.objects.get(user = user)
                self.final_push(user_account,title,message,sender)
                     
        return

    def post(self,request):
        users = request.data['users']
        title = request.data['title']
        message = request.data['message']
        sender = UserAccount.objects.get(user = request.user)
        self.send_notification(users,title,message,sender)
        return Response(status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        user_account = UserAccount.objects.get(user = user)
        notifies  = Notification_table.objects.filter(recieve_user = user_account)
        context = []
        print(notifies)
        for notify in notifies:
            data = {
                "id": notify.id,
                "title": notify.title,
                "message": notify.message,
                "sender": notify.send_user.firstname,
            }
            context.append(data)
        content = paginator.paginate_queryset(context, request)
        return paginator.get_paginated_response(content)
