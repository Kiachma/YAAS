from Auctions.models import Category ,Auction , Bid
from django.contrib import admin
from django import forms
from Auctions.datafiles import AuctionStatus
class AuctionAdmin(admin.ModelAdmin):
    fields = ('name','banned','status')

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ]







admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category, CategoryAdmin)