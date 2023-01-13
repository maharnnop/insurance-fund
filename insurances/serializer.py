from rest_framework import serializers
from .models import Insurance,Invest_insure,User_insure
from accounts.models import User

class InsuranceSerialier(serializers.HyperlinkedModelSerializer):
    insures_invest_insure = serializers.HyperlinkedRelatedField(
        view_name='invest_insure_detail',
        many=True, # one - to many relationship
        read_only=True
    )
    insures_user_insure = serializers.HyperlinkedRelatedField(
        view_name='user_insure_detail',
        many=True, # one - to many relationship
        read_only=True
    )
    # artist_url = serializers.ModelSerializer.serializer_url_field(
    #     view_name="artist_detail"
    # )
    class Meta:
        model = Insurance
        fields =('id','name','descript','img_url','expire_day','release','premium','compensation','fund','init_fund','insures_invest_insure','insures_user_insure')

class InvestInsureSerialier(serializers.HyperlinkedModelSerializer):
    invest = serializers.HyperlinkedRelatedField(
        view_name='user_detail',
        read_only=True,

    )
    invest_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source ='user',
        # many=True
    )
    insure = serializers.HyperlinkedRelatedField(
        view_name='insure_detail',
        read_only=True
    )
    insure_id = serializers.PrimaryKeyRelatedField(
        queryset = Insurance.objects.all(),
        source ='insure',
        # many=True
    )

    # artist_id = serializers.PrimaryKeyRelatedField(
    #     queryset = Artist.objects.all(),
    #     source ='artist'
    # )

    class Meta:
        model = Invest_insure
        fields =( 'id','invest','invest_id','insure_id','insure','cost','revenue')


class UserInsureSerialier(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user_detail',
        read_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source ='user'
    )
    insure = serializers.HyperlinkedRelatedField(
        view_name='insure_detail',
        read_only=True
    )
    insure_id = serializers.PrimaryKeyRelatedField(
        queryset = Insurance.objects.all(),
        source ='user'
    )
    # artist_id = serializers.PrimaryKeyRelatedField(
    #     queryset = Artist.objects.all(),
    #     source ='artist'
    # )

    class Meta:
        model = User_insure
        fields =( 'id','user','user_id','insure','insure_id','date_buy')