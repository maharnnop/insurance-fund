from rest_framework import generics
from .serializer import InsuranceSerialier,InvestInsureSerialier,UserInsureSerialier
from .models import Insurance,Invest_insure,User_insure
from rest_framework.permissions import IsAuthenticated,IsAdminUser

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

class InvestInsureList(generics.ListCreateAPIView):
    queryset = Invest_insure.objects.all()
    serializer_class = InvestInsureSerialier

class UserInsureList(generics.ListCreateAPIView):
    queryset = User_insure.objects.all()
    serializer_class =UserInsureSerialier

class InvestInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invest_insure.objects.all()
    serializer_class = InvestInsureSerialier

class UserInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User_insure.objects.all()
    serializer_class = UserInsureSerialier


