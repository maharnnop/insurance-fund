from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

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
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'users_user_insure', 'users_invest_insure')

class SignUpSerialier(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields =('username', 'email', 'password', 'first_name', 'last_name', 'gender',
                  'date_of_birth')
    
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        username_exists = User.objects.filter(username=attrs['username']).exists()
        #check email already used
        if email_exists:
            raise ValidationError('Email has already used')
        if username_exists:
            raise ValidationError('Username has already used')

        return super().validate(attrs)

    def create(self, validated_data):
        # remove raw password from validated data
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password) # hash password
        user.save()
        Token.objects.create(user=user)
        return user
