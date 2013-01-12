from Auctions.models import Item, Category ,Auction , Bid
from django.contrib import admin
from django.contrib.auth.models import User


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    max_num = 1
class BidderInline(admin.TabularInline):
    model = Bid
    extra = 2

class AuctionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['seller']}),
    ]
    inlines = [ItemInline,BidderInline]

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ]



admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category, CategoryAdmin)