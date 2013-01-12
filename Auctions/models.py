from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Auction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    seller= models.ForeignKey(User, related_name='auction_seller')


    def __unicode__(self):
        return self.item.name
class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    auction= models.OneToOneField(Auction)
    def __unicode__(self):
        return self.name

class Bid(models.Model):
    auction= models.ForeignKey(Auction)
    user = models.ForeignKey(User)
    bid= models.DecimalField(max_digits=9 ,decimal_places=2)







