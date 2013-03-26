# -*- coding: utf-8 -*-
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
from django.utils.translation import ugettext as _
from django.contrib import messages


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
    return render_to_response('auctions/view.html', {'form': form, 'auction': auction}, RequestContext(request))


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
                auction.status = 0
            request.session['auction'] = auction
            return render_to_response('auctions/confirm.html', {}, RequestContext(request))
    else:
        form = AuctionForm
    c = {'form': form}
    return render_to_response('auctions/edit.html', c, RequestContext(request))


@login_required(login_url='/')
def confirm(request):
    if request.method == 'POST':
        if (request.POST['confirm'] == 'True'):
            auction = request.session.get('auction')
            # del request.session['auction']
            auction.save()
            send_mail(_("Auction: ") + auction.name + _(' created'), auction.getAuctionInfo()
                , 'YAAS@YAAS.fi',
                      [auction.seller.email], fail_silently=False)
            return render_to_response('auctions/view.html', {'from': BidForm(), 'auction': auction},
                                      RequestContext(request))
        return HttpResponseRedirect(reverse('index' ,args=('',)))


@login_required(login_url='/')
def delete(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    Auction.delete(auction)
    return HttpResponseRedirect(reverse('index' ,args=('',)))


def sendBidMails(a, bid):
    send_mail(str(bid.bid) + " bid placed on " + a.name, str(bid.bid) + " bid placed on " + a.name, 'YAAS@YAAS.fi',
              [bid.user.email], fail_silently=False)
    send_mail(str(bid.bid) + " bid placed on " + a.name, str(bid.bid) + " bid placed on " + a.name, 'YAAS@YAAS.fi',
              [a.seller.email], fail_silently=False)
    send_mail("You have been overbidden on" + a.name,
              str(bid.bid) + " bid placed on " + a.name + " by " + bid.user.get_full_name(), 'YAAS@YAAS.fi',
              [a.getLatestBid().user.email], fail_silently=False)


@login_required(login_url='/')
def bid(request, auction_id):
    a = Auction.objects.get(pk=auction_id)
    bid = Bid()
    bid.auction = a
    bid.user = request.user
    form = BidForm(request.POST, instance=bid)
    if form.is_valid():
        if a.getLatestBidSum() >= form.instance.bid:
            messages.add_message(request, messages.WARNING, 'Looks like someone was faster than you, please a new bid!')
        else:
            sendBidMails(a, bid)
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Bid placed successfully')
        if a.deadline - timezone.now() < timedelta(minutes=5):
            a.deadline += timedelta(minutes=5)
            a.save()
        return HttpResponseRedirect((reverse('auctions:view', args=(a.id,))))
    return render_to_response('auctions/view.html', {'form': form, 'auction': a}, RequestContext(request))


def sendBanMails(a):
    for bid in a.bid_set.all():
        send_mail(a.name + ' Banned', 'An administrator has banned the action: ' + a.name, 'YAAS@YAAS.fi',
              [bid.user.email], fail_silently=False)
    send_mail(a.name + ' Banned', 'An administrator has banned your action: ' + a.name, 'YAAS@YAAS.fi',
              [a.seller.email], fail_silently=False)


def ban(request, auction_id):
    a = Auction.objects.get(pk=auction_id)
    a.banned = True
    sendBanMails(a)
    a.save()
    return HttpResponseRedirect((reverse('auctions:view', args=(a.id,))))