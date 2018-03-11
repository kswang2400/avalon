from django.contrib.auth.forms import UserCreationForm

from game.models import AvalonUser

class AvalonUserCreationForm(UserCreationForm):
    class Meta:
        model = AvalonUser
        fields = ("username",)