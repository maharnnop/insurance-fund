from rest_framework import generics
from .serializer import InsuranceSerialier,InvestInsureSerialier,UserInsureSerialier
from .models import Insurance,Invest_insure,User_insure

class InsuranceList(generics.ListCreateAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier

class InvestInsureList(generics.ListCreateAPIView):
    queryset = Invest_insure.objects.all()
    serializer_class = InvestInsureSerialier

class UserInsureList(generics.ListCreateAPIView):
    queryset = User_insure.objects.all()
    serializer_class =UserInsureSerialier

class InsuranceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier

class InvestInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invest_insure.objects.all()
    serializer_class = InvestInsureSerialier

class UserInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User_insure.objects.all()
    serializer_class = UserInsureSerialier


