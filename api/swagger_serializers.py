from rest_framework import serializers

from cabinet.models import AdvUser


class AccessTokenSeriazels(serializers.Serializer):
    accessToken = serializers.CharField(read_only=True, help_text='new access Token')
    refreshToken = serializers.CharField(read_only=True, help_text='new refresh Token')

    class Meta:
        ref_name = None  # prohibiting the transfer of the function name to the front


class ErrorsList(serializers.Serializer):
    code = serializers.IntegerField(read_only=True, help_text='error code')
    message = serializers.CharField(read_only=True, help_text='error message')

    class Meta:
        ref_name = None  # prohibiting the transfer of the function name to the front


class ResponceError(serializers.Serializer):
    errors = serializers.ListSerializer(child=ErrorsList())
    description = serializers.CharField(read_only=True, help_text='description')

    class Meta:
        ref_name = None  # prohibiting the transfer of the function name to the front


class UserSerializerSwagger(serializers.ModelSerializer):

    class Meta:
        model = AdvUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'birthday',
                  'age', 'language', 'status', 'created_at', 'updated_at')
        ref_name = None  # prohibiting the transfer of the function name to the front


class UsersListSerializerSwagger(serializers.Serializer):
    users = serializers.ListSerializer(child=UserSerializerSwagger())

    class Meta:
        ref_name = None  # prohibiting the transfer of the function name to the front