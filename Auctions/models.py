# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from Auctions.datafiles import AuctionStatus
from django.db.models import Max
from django import forms
from django.utils.translation import ugettext as _
from decimal import Decimal


class CustomUser(User):
    language = models.CharField(max_length=100)
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Auction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(CustomUser, related_name='auction_seller')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length=200)
    min_price = models.DecimalField(decimal_places=2, max_digits=10)
    deadline = models.DateTimeField()
    status = models.PositiveSmallIntegerField(null=True)
    banned = models.NullBooleanField(null=True)
    version = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def getAuctionInfo(self):
        return _('\n Auction name:') + self.name + \
               _('\n Description: ') + self.description + \
               _('\n Category: ' + self.category.name) + \
               _('\n Min price: ') + str(self.min_price) + \
               _('\n Deadline: ') + str(self.deadline)


    def getStatus(self):
        if self.banned:
            return AuctionStatus.banned
        if self.status == AuctionStatus.adjudicated:
            return AuctionStatus.adjudicated
        elif self.deadline > timezone.now():
            return AuctionStatus.active
        else:
            return AuctionStatus.due

    def getStatusString(self):
        return AuctionStatus.getName(self.getStatus())


    def getLatestBid(self):
        if not self.bid_set.all():
            return None
        bid = self.bid_set.all().latest('bid')
        return bid


    def getLatestBidSum(self):
        bid = self.bid_set.all().latest('bid')
        return bid.bid

    def clean_deadline(self):
        data = self.cleaned_data['deadline']
        if ~(data > timezone.now()(hours=72)):
            raise forms.ValidationError("The duration of the auction has to be at least 72h")
        return data


class Bid(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(Auction)
    user = models.ForeignKey(CustomUser)
    bid = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
        return str(self.bid) + ' - ' + self.user.first_name + ' ' + self.user.last_name

    def getLatestBidSum(self):
        return str(self.bid)

    def clean(self):
        from django.core.exceptions import ValidationError
        # Don't allow draft entries to have a pub_date.
        auction = self.auction
        if auction.getLatestBid():
            if self.bid < auction.getLatestBid().bid + self.to_decimal(0.01):
                raise ValidationError("The new bid has to raise the old one by at least 0,01")
        if self.bid < auction.min_price:
            raise ValidationError("A bid must be higher than the minimum price")
        return self.bid

    def to_decimal(self, float_price):
        return Decimal('%.2f' % float_price)


