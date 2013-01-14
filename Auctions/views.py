from django.template import RequestContext
from django.shortcuts import render
from Auctions.models import Auction
from Auctions.forms import AuctionForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def index(request):
    latest_auction_list = Auction.objects.order_by('created')[:5]
    context = {'latest_auction_list': latest_auction_list}
    return render(request, 'auctions/index.html', context)


def detail(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    form = AuctionForm(instance=auction)
    return render_to_response('auctions/detail.html' ,{'form': form,'auction' : auction}, RequestContext(request))

def save(request, auction_id):
    if request.method == 'POST':
        a = Auction.objects.get(pk=auction_id)
        form = AuctionForm(request.POST,instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/auctions/%s/' %auction_id)
    else:
        form = AuctionForm
        c={'form': form}
    return render_to_response('auctions/detail.html',c , RequestContext(request))