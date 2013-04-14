# -*- coding: utf-8 -*-
from django.template import RequestContext
from Auctions.models import Auction, Bid
from Auctions.forms import *
from Auctions.datafiles import AuctionStatus
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
from decimal import Decimal
from django import forms


@login_required(login_url='/')
def edit(request, auction_id):
    if auction_id == u'None':
        auction = Auction()
        form = AuctionForm(instance=auction)
        auction.seller = request.user
        form = AuctionForm()
    else:
        auction = Auction.objects.get(pk=auction_id)
        form = EditAuctionForm(instance=auction)
    return render_to_response('auctions/edit.html', {'form': form, 'auction': auction}, RequestContext(request))


def view(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return render_to_response('auctions/view.html', { 'auction': auction,'form':BidForm()}, RequestContext(request))


@login_required(login_url='/')
def save(request, auction_id):
    if request.method == 'POST':
        if auction_id == u'None' or auction_id=='':
            form = AuctionForm(request.POST)
        else:
            a = Auction.objects.get(pk=auction_id)
            a.version += 1
            form = EditAuctionForm(request.POST, instance=a)
            form.save()
            return HttpResponseRedirect(reverse('auctions:view' ,args=(a.id,)))
        if form.is_valid() :
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
            del request.session['auction']
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
    if a.getLatestBid() is not None:
        send_mail("You have been overbidden on" + a.name,
              str(bid.bid) + " bid placed on " + a.name + " by " + bid.user.get_full_name(), 'YAAS@YAAS.fi',
              [a.getLatestBid().user.email], fail_silently=False)


def to_decimal(float_price):
    return Decimal('%.2f' % float_price)


@login_required(login_url='/')
def bid(request, auction_id):
    a = Auction.objects.get(pk=auction_id)
    bid=Bid()
    bid.auction = a
    bid.user = request.user
    form = BidForm(request.POST,instance=bid)
    if request.method == 'POST' and form.is_valid():

        edited_version = int(request.POST["edited_version"])

        if edited_version != a.version:
            messages.add_message(request, messages.WARNING, 'The auctions description has changed since you placed your bid, please re-read the description and replace your bid')
        # elif a.getLatestBid():
        #     if int(bid.bid)<a.getLatestBid().bid + to_decimal(0.01):
        #         messages.add_message(request, messages.WARNING, 'The new bid has to raise the old one by at least 0,01')
        elif timezone.now()>=a.deadline or a.banned==False or a.getStatus()==AuctionStatus.adjudicated or a.getStatus()==AuctionStatus.due:
            messages.add_message(request, messages.WARNING, 'The auction is Banned/Due/Adjudicated')
        # elif int(bid.bid) < a.min_price:
        #      raise forms.ValidationError("A bid must be higher than the minimum price")

        else:

            form.save()

            sendBidMails(a, bid)
            messages.add_message(request, messages.SUCCESS, 'Bid placed successfully')
            if a.deadline - timezone.now() < timedelta(minutes=5):
                a.deadline += timedelta(minutes=5)
                a.save()
        return HttpResponseRedirect((reverse('auctions:view', args=(a.id,))))
    return render_to_response('auctions/view.html', {'auction': a,'form':form}, RequestContext(request))




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