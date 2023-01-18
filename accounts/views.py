from rest_framework import generics, status
from .serializer import UserSerialier,SignUpSerialier
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

from django.http import JsonResponse
from django.conf import settings
from django.core import serializers
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.utils import simplejwt_decode_handler\
import jwt
# from rest_framework_jwt.utils import jwt_decode_handler
User = get_user_model()


def create_jwt(user: User):
    refresh = RefreshToken.for_user(user)

    tokens = {"access": str(refresh.access_token), "refresh": str(refresh), 'username':user.username}

    return tokens

class SignUpView(generics.CreateAPIView):
   serializer_class = SignUpSerialier
   permission_classes = []
   
   def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            user =User.objects.get(username = serializer.data['username'])
            token = create_jwt(user)
            response = {"message": "User Created Successfully", "token":token}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt(user)
            decoded_payload = jwt.decode(tokens['access'], settings.SECRET_KEY)

            response = {"message": "Login Successfull", 
            "token": tokens,
            "decode":decoded_payload}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid username or password"},status=status.HTTP_409_BAD_REQUEST)

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)

class UserList(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class =UserSerialier
    def get(self, request: Request):
        queryset = User.objects.all()
        response = serializers.serialize("json", queryset)
        # queryset = json_serializer.serialize(User.objects.all())
        # header = request.headers
        # response = {"message": "User Created Successfully", "data": queryset,"header":header}

        # return Response(data=response, status=status.HTTP_201_CREATED)
        return  JsonResponse(response, safe=False)
        
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerialier