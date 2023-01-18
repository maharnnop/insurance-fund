from rest_framework import serializers
from .models import Insurance,Invest_insure,User_insure
from rest_framework.request import Request
from accounts.models import User

class InvestInsureSerialier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invest_insure
        fields =( 'id','invest_id','insure_id','cost','revenue')


class UserInsureSerialier(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User_insure
        fields =( 'id','user_id','insure_id','date_buy')

class InsuranceSerialier(serializers.HyperlinkedModelSerializer):
    # insures_invest_insure = serializers.HyperlinkedRelatedField(
    #     view_name='invest_insure_detail',
    #     many=True, # one - to many relationship
    #     read_only=True
    # )
    insures_user_insure = UserInsureSerialier(many=True, read_only=True)
    insures_invest_insure = InvestInsureSerialier(many=True, read_only=True)
    # insures_user_insure = serializers.HyperlinkedRelatedField(
    #     view_name='user_insure_detail',
    #     many=True, # one - to many relationship
    #     read_only=True
    # )
    # artist_url = serializers.ModelSerializer.serializer_url_field(
    #     view_name="artist_detail"
    # )
    class Meta:
        model = Insurance
        fields =('id','name','descript','img_url','expire_day','release','premium','compensation','fund','init_fund','insures_invest_insure','insures_user_insure')

