from rest_framework import generics,status
from .serializer import InsuranceSerialier,InvestInsureSerialier,UserInsureSerialier
from .models import Insurance,Invest_insure,User_insure
from rest_framework.permissions import IsAuthenticated,IsAdminUser
import jwt
from django.conf import settings
from rest_framework.response import Response
from django.core import serializers
from rest_framework.views import APIView

class InsuranceList(generics.ListAPIView):
    permission_classes=[]
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier
    
class InsuranceCreate(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier

class InsuranceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier

class InvestInsureList(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        # return super().post(request, *args, **kwargs)
        if request.data['invest_id'] == user_id:
            form = InvestInsureSerialier(data=request.data)
            if form.is_valid():
                form.save()
            return Response(({'message : create successful'},request.data))
        else: return Response({'massage : crate only own data'}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        queryset = Invest_insure.objects.filter(invest_id =user_id).values()
        return Response((queryset,{'user_id':user_id}))

class UserInsureList(APIView):
    permission_classes=[IsAuthenticated]
    # queryset = User_insure.objects.all()
    # serializer_class =UserInsureSerialier
    def post(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        if request.data['invest_id'] == user_id:
            form = UserInsureSerialier(data=request.data)
            if form.is_valid():
                form.save()
            return Response(({'message : create successful'},request.data))
        else: return Response({'massage : crate only own data'}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        queryset = User_insure.objects.filter(invest_id =user_id).values()
        return Response((queryset,{'user_id':user_id}))

class InvestInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[]
    queryset = Invest_insure.objects.all()
    serializer_class = InvestInsureSerialier

class UserInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[]
    queryset = User_insure.objects.all()
    serializer_class = UserInsureSerialier


