from rest_framework import generics, status
from .serializer import InsuranceSerialier, InvestInsureSerialier, UserInsureSerialier
from .models import Insurance, Invest_insure, User_insure
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import jwt
from django.conf import settings
from rest_framework.response import Response
from django.core import serializers
from rest_framework.views import APIView
from django.db.models import Subquery, OuterRef,Sum,Value,IntegerField
from django.db.models.functions import Cast, Coalesce

def update_fund():
    total_cost = Invest_insure.objects.values("insure_id").annotate(sum=Sum('cost'))
    Insurance.objects.update(fund=Subquery(total_cost.filter(insure_id=OuterRef('id')).values('sum')))

class InsuranceList(generics.ListAPIView):
    permission_classes = []
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier


class InsuranceCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier


class InsuranceDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier


class InvestInsureList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        # return super().post(request, *args, **kwargs)
        if request.data['invest_id'] == user_id:
            form = InvestInsureSerialier(data=request.data)
            if form.is_valid():
                form.save()
            update_fund()
            return Response(({'message : create successful'}, request.data))
        else:
            return Response({'massage : crate only own data'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        queryset = Invest_insure.objects.filter(invest_id=user_id).values()
        return Response((queryset, {'user_id': user_id}))


class UserInsureList(APIView):
    permission_classes = [IsAuthenticated]
    # queryset = User_insure.objects.all()
    # serializer_class =UserInsureSerialier

    def post(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        if request.data['invest_id'] == user_id:
            form = UserInsureSerialier(data=request.data)
            if form.is_valid():
                form.save()
            return Response(({'message : create successful'}, request.data))
        else:
            return Response({'massage : crate only own data'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        queryset = User_insure.objects.filter(invest_id=user_id).values()
        return Response((queryset, {'user_id': user_id}))


class InvestInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Invest_insure.objects.all()
    serializer_class = InvestInsureSerialier

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        queryset = Invest_insure.objects.filter(id=pk).values()
        return Response(queryset)

    def update(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        pk = self.kwargs.get('pk')
        old = Invest_insure.objects.get(id=pk)
        if request.data['invest_id'] == user_id:
            form = InvestInsureSerialier(data=request.data, instance=old)
            if form.is_valid():
                old = form.save()
                update_fund()
            return Response(({'message : update successful'}, request.data))
        else:
            return Response({'massage : update only own data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        pk = self.kwargs.get('pk')
        invest_id  = Invest_insure.objects.get(id=pk).invest_id
        if invest_id == user_id:
            Invest_insure.objects.get(id=pk).delete()
            update_fund()
            return Response({f'message : delete id:{pk} successful'})
        else:
            return Response({'massage : update only own data',invest_id}, status=status.HTTP_400_BAD_REQUEST)
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)


class UserInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User_insure.objects.all()
    serializer_class = UserInsureSerialier
