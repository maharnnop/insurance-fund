from rest_framework import serializers
from .models import User


class UserSerialier(serializers.HyperlinkedModelSerializer):
    users_invest_insure = serializers.HyperlinkedRelatedField(
        view_name='invest_insure_detail',
        many=True,  # one - to many relationship
        read_only=True
    )
    users_user_insure = serializers.HyperlinkedRelatedField(
        view_name='user_insure_detail',
        many=True,  # one - to many relationship
        read_only=True
    )
    # artist_url = serializers.ModelSerializer.serializer_url_field(
    #     view_name="artist_detail"
    # )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'users_user_insure', 'users_invest_insure')
