# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from Auctions.datafiles import AuctionStatus
from django.db.models import Max
from django import forms
from django.utils.translation import ugettext as _

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Auction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    seller= models.ForeignKey(User, related_name='auction_seller')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length=200)
    min_price = models.DecimalField(decimal_places=2,max_digits=10)
    deadline = models.DateTimeField()
    status = models.PositiveSmallIntegerField(null=True)
    banned = models.NullBooleanField(null=True)

    def __unicode__(self):
        return self.name
    def getAuctionInfo(self):
        return _('\n Auction name:')+ self.name + \
               _( '\n Description: ') +self.description+\
               _('\n Category: '+self.category.name)+\
               _('\n Min price: ')+str(self.min_price)+\
               _('\n Deadline: ')+ str(self.deadline)


    def getStatus(self):
        if self.banned:
            return AuctionStatus.banned
        if self.status == AuctionStatus.adjudicated:
            return AuctionStatus.adjudicated
        elif self.deadline>timezone.now():
            return AuctionStatus.active
        else:
            return AuctionStatus.due

    def getStatusString(self):
        return AuctionStatus.getName(self.getStatus())


    def getLatestBid(self):
        bid= self.bid_set.latest('bid')
        return bid


    def getLatestBidSum(self):
        bid= self.bid_set.latest('bid')
        return bid.bid

    def clean_deadline(self):
        data = self.cleaned_data['deadline']
        if ~(data>timezone.now() (hours = 72)):
            raise forms.ValidationError("The duration of the auction has to be at least 72h")
        return data



class Bid(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    auction= models.ForeignKey(Auction)
    user = models.ForeignKey(User)
    bid= models.DecimalField(max_digits=9 ,decimal_places=2)
    def __unicode__(self):
        return str(self.bid)+ ' - ' +self.user.first_name + ' '+ self.user.last_name
    def getLatestBidSum(self):
        return str(self.bid)






