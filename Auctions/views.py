import bzrlib.commit
from django.template import RequestContext
from Auctions.models import Auction, Bid
from Auctions.forms import AuctionForm, BidForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

@login_required(login_url='/')
def edit(request, auction_id):
    if auction_id == u'None':
        auction = Auction()
        form = AuctionForm(instance=auction)
        auction.seller = request.user
        form = AuctionForm()
    else:
        auction = Auction.objects.get(pk=auction_id)
        form = modelform_factory(Auction, form=AuctionForm, exclude=('seller', 'category',))
    return render_to_response('auctions/edit.html', {'form': form, 'auction': auction}, RequestContext(request))


def view(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    form = BidForm()
    return render_to_response('auctions/view.html', {'form':form , 'auction': auction}, RequestContext(request))

@login_required(login_url='/')
def save(request, auction_id):
    if request.method == 'POST':
        if auction_id == u'None':
            form = AuctionForm(request.POST)
        else:
            a = Auction.objects.get(pk=auction_id)
            form = AuctionForm(request.POST, instance=a)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            if form.instance.id is None:
                send_mail('Auction: '+ auction.name +' created' , 'Auction INFO', 'YAAS@YAAS.fi',
                    [auction.seller.email], fail_silently=False)
                auction.status=0
            auction.save()
            request.session['auction'] = auction
            return render_to_response('auctions/confirm.html', {}, RequestContext(request))
    else:
        form = AuctionForm
    c = {'form': form}
    return render_to_response('auctions/edit.html', c, RequestContext(request))


@login_required(login_url='/')
def confirm(request):
    auction= request.session.get('auction')
    auction.save()
    return render_to_response('auctions/view.html', {'from':BidForm(),'auction': auction}, RequestContext(request))

@login_required(login_url='/')
def delete(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    Auction.delete(auction)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/')
def bid(request, auction_id):
    a = Auction.objects.get(pk=auction_id)
    bid= Bid()
    bid.auction=a
    bid.user=request.user
    form = BidForm(request.POST,instance=bid)
    if form.is_valid():
        form.save()
        if a.deadline-timezone.now()<timedelta(minutes=5):
            auction_id.deadline+=timedelta(minutes=5)
        return HttpResponseRedirect((reverse('auctions:view',args=(a.id,))))
    return render_to_response('auctions/view.html', {'form':form,'auction': a}, RequestContext(request))


