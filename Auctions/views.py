from django.http import HttpResponse
from Auctions.models import Auction

def index(request):
    latest_auction_list = Auction.objects.order_by('item.name')[:5]
    output = ', '.join([p.item.name for p in latest_auction_list])
    return HttpResponse(output)