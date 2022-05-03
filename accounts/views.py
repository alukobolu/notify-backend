from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token

class deleting_auth_key(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 
    def get(self,request):
        try:
            request.user.auth_token.delete()
            data ={}
            data["Success"]     = "Token Deleted"
            return Response(data=data)
        except:
            data ={}
            data["Error"]     = "User token doesn't exist"
            return Response(data=data)
class CheckEmail (APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            email = request.data('email')
            user = User.objects.get(email = email)
            return Response(True)
        except:
            return Response(False)

# Sign Up View
class SignUp (APIView):
    permission_classes = [AllowAny]

    # serializer_class = UserRegistrationSerializer
    def creation_of_key(self,userAccount):
        token = Token.objects.get_or_create(user=userAccount.user)
        return token

    def creating_auth_key(self,email):
        try:
            user = UserAccount.objects.get(email=email)
            token  = self.creation_of_key(user)
            instance =  TokenList()
            print(token)
            instance.token = token[0].key
            instance.user = user
            instance.save()
            return token[0].key
        except:
            return "Sorry something went wrong"

    def post(self, request):
        data = {}

        _email = request.data['email']

        password = request.data['password']
        firstname = request.data['firstname']
        expo_push_token = request.data['expoT']

        if User.objects.filter(email=_email).exists():

            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            email=_email,
        )

        user.set_password(password)
        user.save()

        user_account = UserAccount(
            user=user, email=user.email, firstname=firstname, expo_push_token=expo_push_token)
        user_account.save()
        
        data['token'] = self.creating_auth_key(user.email)
        data['response'] = 'Registered Successfully'
        return Response(data)

class UpdateDetails(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        user = request.user

        account = UserAccount.objects.get(user=user)

        data = request.data

        account.firstname = data['firstname']

        account.save(update_fields=['firstname'])

        return Response(status=status.HTTP_200_OK)

