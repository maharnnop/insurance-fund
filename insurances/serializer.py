from rest_framework import serializers
from .models import Insurance,Invest_insure,User_insure

class InsuranceSerialier(serializers.HyperlinkedModelSerializer):
    invest_insure = serializers.HyperlinkedRelatedField(
        view_name='invest_insure_detail',
        many=True, # one - to many relationship
        read_only=True
    )
    user_insure = serializers.HyperlinkedRelatedField(
        view_name='user_insure_detail',
        many=True, # one - to many relationship
        read_only=True
    )
    # artist_url = serializers.ModelSerializer.serializer_url_field(
    #     view_name="artist_detail"
    # )
    class Meta:
        model = Insurance
        fields =('id','name','descript','img_url','expire_day','release','premium','compensation','fund','init_fund','user_insure','invest_insure')

class InvestInsureSerialier(serializers.HyperlinkedModelSerializer):
    invest = serializers.HyperlinkedRelatedField(
        view_name='user_detail',
        read_only=True
    )
    
    insure = serializers.HyperlinkedRelatedField(
        view_name='insure_detail',
        read_only=True
    )

    # artist_id = serializers.PrimaryKeyRelatedField(
    #     queryset = Artist.objects.all(),
    #     source ='artist'
    # )

    class Meta:
        model = Invest_insure
        fields =( 'id','invest','insure','cost','revenue')


class UserInsureSerialier(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='artist_detail',
        read_only=True
    )

    insure = serializers.HyperlinkedRelatedField(
        view_name='artist_detail',
        read_only=True
    )
    # artist_id = serializers.PrimaryKeyRelatedField(
    #     queryset = Artist.objects.all(),
    #     source ='artist'
    # )

    class Meta:
        model = User_insure
        fields =( 'id','user','insure','date_buy')