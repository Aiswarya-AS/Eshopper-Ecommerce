from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','phone','password1','password2']