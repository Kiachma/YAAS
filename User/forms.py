from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password')
        widgets = {
            'password': PasswordInput(),
            }


