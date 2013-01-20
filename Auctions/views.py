from django.template import RequestContext
from django.shortcuts import render
from Auctions.models import Auction
from Auctions.forms import AuctionForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail



def detail(request, auction_id):
    if auction_id ==u'None':
        auction=Auction()
        auction.seller=request.user
    else:
        auction = Auction.objects.get(pk=auction_id)
    form = AuctionForm(instance=auction)
    return render_to_response('auctions/detail.html' ,{'form': form,'auction' : auction}, RequestContext(request))

def save(request, auction_id):
    if request.method == 'POST':
        if auction_id==u'None':
            form=AuctionForm(request.POST)
        else:
            a = Auction.objects.get(pk=auction_id)
            form = AuctionForm(request.POST,instance=a)
        if form.is_valid():
            if form.instance.id is None:
                send_mail('Subject here', 'Here is the message.', 'from@example.com',
                    ['to@example.com'], fail_silently=False)
            form.save()
            return HttpResponseRedirect('/auctions/%s/' %form.instance.id)
    else:
        form = AuctionForm
    c={'form': form}
    return render_to_response('auctions/detail.html',c , RequestContext(request))

def delete(request, auction_id):
    auction=Auction.objects.get(pk=auction_id)
    Auction.delete(auction)
    return HttpResponseRedirect(reverse('index'))