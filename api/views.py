import re

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi

from api.api_error_list import response_api_error
from api.serializers import UserSerializer, UserRegisterSerializer
from api.swagger_serializers import AccessTokenSeriazels, ResponceError, UsersListSerializerSwagger, \
    UserSerializerSwagger
from cabinet.models import AdvUser
import jwt


# API User registration / authorization
from web_service.settings import SECRET_KEY


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_id='user registration / authorization',
        security=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='username',
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='password'
                )
            }
        ),
        responses={
            200: AccessTokenSeriazels(),
            400: ResponceError()
        },
        tags=['User']
    )
    def post(self, request):
        data = request.data
        # if the user does not exist, create user tokens
        serializer = UserRegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        res = {
            "accessToken": str(refresh.access_token),
            "refreshToken": str(refresh),
        }
        return Response(res, status.HTTP_201_CREATED)




# API Refresh JWT TOKEN CBV controller

class RefreshTokenUserAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_id='user refresh token',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='refresh token',
                )
            }
        ),
        responses={
            200: AccessTokenSeriazels(),
            400: ResponceError()
        },
        tags=['User']
    )
    def post(self, request):
        data = request.data
        try:
            data = jwt.decode(data["refresh"], SECRET_KEY, algorithms=['HS256'])
            current_user = AdvUser.objects.filter(pk=data["user_id"]).first()
            if current_user:
                refresh = RefreshToken.for_user(current_user)
                res = {
                    "accessToken": str(refresh.access_token),
                    "refreshToken": str(refresh),
                }
                return Response(res, status.HTTP_201_CREATED)
            else:
                res = {
                    "errors": response_api_error(2)
                }
                return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {
                "errors": response_api_error(3),
                "description": str(e)
            }
            return Response(res, status.HTTP_400_BAD_REQUEST)


class UsersAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_id='user list',
        manual_parameters=[
            openapi.Parameter(
                name='lang', in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Parameters for filter: by lang (choice)"
            ),
            openapi.Parameter(
                name='age', in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Parameters for filter: by age"
            ),
            openapi.Parameter(
                name='search', in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Parameters for search: email, phone, first_name, last_name."
            ),
        ],
        responses={
            200: UsersListSerializerSwagger(),
            400: ResponceError()
        },
        tags=['User']
    )
    def get(self, request):
        if 'lang' in request.GET:
            language = request.GET['lang']
            users = AdvUser.objects.exclude(status=request.user.status).filter(language=language).\
                order_by('first_name', 'last_name')
        elif 'age' in request.GET:
            age = request.GET['age']
            users = AdvUser.objects.exclude(status=request.user.status).filter(age=age).\
                order_by('first_name', 'last_name')
        elif 'age' in request.GET and 'lang' in request.GET:
            language = request.GET['lang']
            age = request.GET['age']
            users = AdvUser.objects.exclude(status=request.user.status).\
                filter(age=age).filter(language=language).order_by('first_name','last_name')
        else:
            users = AdvUser.objects.exclude(status=request.user.status).order_by('first_name', 'last_name')

        serializer = UserSerializer(users, many=True)
        res = {
            'error': False,
            'users': serializer.data
        }
        return Response(res, status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_id='user detail',
        responses={
            200: UserSerializerSwagger(),
            400: ResponceError()
        },
        tags=['User']
    )
    def get(self, request, pk):
        try:
            user_ = AdvUser.objects.get(pk=pk)
            serializer = UserSerializer(user_, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        except AdvUser.DoesNotExist:
            res = {
                "errors": response_api_error(404)
            }
            return Response(res, status.HTTP_400_BAD_REQUEST)





# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMzI0NzMxLCJpYXQiOjE2MzUwMTExMzEsImp0aSI6IjhjNzU0YTNiNmZkODQ3NzJhODRkYjMwMGUxODE2MmY5IiwidXNlcl9pZCI6NH0.pI6Tlvq0I30co6S3p6JdC7PU3z3_5i7_QqoUb6XLKr0

"""
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMzI0NzMxLCJpYXQiOjE2MzUwMTExMzEsImp0aSI6IjhjNzU0YTNiNmZkODQ3NzJhODRkYjMwMGUxODE2MmY5IiwidXNlcl9pZCI6NH0.pI6Tlvq0I30co6S3p6JdC7PU3z3_5i7_QqoUb6XLKr0",
  "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMTMyNDczMSwiaWF0IjoxNjM1MDExMTMxLCJqdGkiOiJhNDcwZDE0NzA2YTI0ZGM2YTFkM2Q3ZjhhMzEwOTViYSIsInVzZXJfaWQiOjR9.rhhZlwakU-ovw7g4sGaSGVBeWzTb0yjQ0_bH41DDP3c"
}
22
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxNDk4ODM4LCJpYXQiOjE2MzUxODUyMzgsImp0aSI6ImM3YWE5ODQ4Yzg0MzRmYmZhYWNiZTdkYjJjMGQ1ODExIiwidXNlcl9pZCI6Nn0.atpokNPo9TOLFHhTkHcT01u4qOh3yn5OKehGwCS91b0",
  "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMTQ5ODgzOCwiaWF0IjoxNjM1MTg1MjM4LCJqdGkiOiJkNTY3ZjAwOTZlYmY0ZDEzYWVhNmY4OTZhNTEyMDVkNiIsInVzZXJfaWQiOjZ9.hktjx5QWEchQb0ZJm0LDDsJoKoiKC3i1tixZ-j-mmbc"
}



"""
