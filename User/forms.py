from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from django.forms.extras.widgets import Select

from Auctions.models import CustomUser


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].widget.attrs['readonly'] = True

    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email', 'password','language')
        from django.conf import settings
        supported = dict(settings.LANGUAGES)
        widgets = {
            'password': PasswordInput(),
            'language': Select(choices=supported.items())
            }


