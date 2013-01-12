
from django.http import Http404
from django.shortcuts import render
from Auctions.models import Auction,Bid

def index(request):
    latest_auction_list = Auction.objects.order_by('created')[:5]
    context = {'latest_auction_list': latest_auction_list}
    return render(request, 'auctions/index.html', context)


def detail(request, auction_id):
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        raise Http404
    return render(request, 'auctions/detail.html', {'auction': auction})