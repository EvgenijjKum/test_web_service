from django.conf.urls import url
from django.urls import path, include

from api.views import UsersAPIView, RefreshTokenUserAPIView, CreateUserAPIView, UserAPIView

app_name = 'api'

urlpatterns = [
    # User
    path('register/', CreateUserAPIView.as_view()),
    path('users/', UsersAPIView.as_view()),

    path('users/<int:pk>/', UserAPIView.as_view()),
    # JWT
    path('user-refresh-token/', RefreshTokenUserAPIView.as_view(), name='token_refresh'),

]
