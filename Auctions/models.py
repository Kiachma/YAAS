# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from Auctions.datafiles import AuctionStatus
from django.db.models import Max
from django import forms

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
        bid= self.bid_set.annotate(Max('bid'))
        if bid.count()==0:
            return None
        return bid[0]

    def clean_deadline(self):
        data = self.cleaned_data['deadline']
        if data<timezone.now():
            raise forms.ValidationError("Deadline has to be a date in the future")
        return data



class Bid(models.Model):
    auction= models.ForeignKey(Auction)
    user = models.ForeignKey(User)
    bid= models.DecimalField(max_digits=9 ,decimal_places=2)
    def __unicode__(self):
        return self.user.first_name + ' '+ self.user.last_name + ' - ' +str(self.bid)





