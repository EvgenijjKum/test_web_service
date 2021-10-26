from rest_framework import serializers
from cabinet.models import AdvUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvUser
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups',
                   'user_permissions']


class UserRegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = AdvUser
        fields = '__all__'

