from rest_framework import generics, status
from .serializer import UserSerialier,SignUpSerialier
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerialier


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerialier

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialier