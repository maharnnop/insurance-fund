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

def update_fund(insure_id):
    total_cost = Invest_insure.objects.filter(insure_id=insure_id).aggregate(Sum('cost'))
    # Insurance.objects.update(fund=Subquery(total_cost.filter(insure_id=OuterRef('id')).values('sum')))
    Insurance.objects.filter(id=insure_id).update(fund=total_cost['cost__sum'])
    qureyset = Insurance.objects.filter(id=insure_id).values_list('fund','init_fund')
    # if qureyset[0]['fund'] >= qureyset[0]['init_fund']:
    if qureyset[0][0] >= qureyset[0][1]:
        Insurance.objects.filter(id=insure_id).update(release=True)

class InsuranceList(generics.ListAPIView):
    permission_classes = []
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier


class InsuranceCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier


class InsuranceDetail(generics.RetrieveAPIView):
    permission_classes = []
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier

class InsuranceUpdate_Del(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerialier


class InvestInsureList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        invest = request.data
        if request.data['invest_id'] == user_id:
            serializer = InvestInsureSerialier(data=invest)
            if serializer.is_valid():
                invest_saved = serializer.save()
                update_fund(invest['insure_id'])
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
        if request.data['user_id'] == user_id:
            form = UserInsureSerialier(data=request.data)
            if form.is_valid():
                form.save()
                return Response(({'message : create successful'}, request.data))
        else:
            return Response({'massage : crate only own data'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        queryset = User_insure.objects.filter(user_id=user_id).values()
        return Response((queryset, {'user_id': user_id}))


class InvestInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvestInsureSerialier

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        queryset = Invest_insure.objects.filter(id=pk).values()
        return Response(queryset)
  
    def patch(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        pk = self.kwargs.get('pk')
        saved_invest = Invest_insure.objects.get(id=pk)
        data = request.data
        serializer = InvestInsureSerialier(instance=saved_invest, data=data,partial=True)
        if request.data['invest_id'] == user_id:
            if serializer.is_valid():
                invest_saved = serializer.save()
                update_fund(saved_invest.insure_id)
            return Response(({'message : update successful'}))
        else:
            return Response({'massage : update only own data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        pk = self.kwargs.get('pk')
        invest_id  = Invest_insure.objects.get(id=pk).invest_id
        if invest_id == user_id:
            Invest_insure.objects.get(id=pk).delete()
            # update_fund()
            return Response({f'message : delete id:{pk} successful'})
        else:
            return Response({'massage : update only own data',invest_id}, status=status.HTTP_400_BAD_REQUEST)
  


class UserInsureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User_insure.objects.all()
    serializer_class = UserInsureSerialier

    # def get(self, request, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     queryset = User_insure.objects.get(id=pk)
    #     form = UserInsureSerialier(instance=queryset)
    #     # form.is_valid()
    #     return Response(form.data)
    #     # return Response(form.d)
    def update(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        pk = self.kwargs.get('pk')
        instance = self.get_object()
        instance.id = request.data.get("pk")
        instance.save()
        if request.data['user_id'] == user_id:
            serializer = self.get_serializer(data=instance)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({'massage : update only own data'}, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, *args, **kwargs):
        header = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(header, settings.SECRET_KEY)['user_id']
        pk = self.kwargs.get('pk')
        req_id  = User_insure.objects.get(id=pk).user_id
        if req_id == user_id:
            User_insure.objects.get(id=pk).delete()
            # update_fund()
            return Response({f'message : delete id:{pk} successful'})
        else:
            return Response({'massage : update only own data',user_id}, status=status.HTTP_400_BAD_REQUEST)
