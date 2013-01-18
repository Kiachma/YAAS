from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'password': PasswordInput(),
            }
