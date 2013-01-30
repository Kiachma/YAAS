from django.forms import ModelForm
from Auctions.models import Auction,Bid
from django.db import models
from django.utils import timezone
from django import forms
from datetime import timedelta
from decimal import Decimal

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%d/%m/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield


class AuctionForm(ModelForm):
    formfield_callback = make_custom_datefield
    class Meta:
        model = Auction
        fields = ('name','category','description','deadline','min_price')
    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline-timezone.now()< timedelta(hours = 72):
            raise forms.ValidationError("The duration of the auction has to be at least 72h")
        return deadline

class BidForm(ModelForm):
    class Meta:
        model = Bid
        exclude=('auction','user')
    def clean_bid(self):
        newBid = self.cleaned_data['bid']
        auction = self.instance.auction
        if newBid<auction.getLatestBid().bid+self.to_decimal(0.01):
            raise forms.ValidationError("The new bid has to raise the old one by at least 0,01")
        if newBid<auction.min_price:
            raise forms.ValidationError("A bid must be higher than the minimum price")
        return newBid
    def to_decimal(self,float_price):
        return Decimal('%.2f' % float_price)