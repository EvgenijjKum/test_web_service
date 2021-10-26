from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AdvUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AdvUser
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = AdvUser
        fields = "__all__"
