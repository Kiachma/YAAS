from django.forms import ModelForm
from Auctions.models import Auction

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
