from django.forms import ModelForm
from Auctions.models import Auction
from django.db import models


def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%d/%m/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield


class AuctionForm(ModelForm):
    formfield_callback = make_custom_datefield
    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        self.fields['seller'].widget.attrs['readonly'] = True
        if self.instance.id:
            self.fields['category'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['deadline'].widget.attrs['readonly'] = True
            self.fields['min_price'].widget.attrs['readonly'] = True

    class Meta:
        model = Auction
        fields = ('name', 'seller','category','description','deadline','min_price')
