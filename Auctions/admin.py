from Auctions.models import Category ,Auction , Bid
from django.contrib import admin

class BidderInline(admin.TabularInline):
    model = Bid
    extra = 2

class AuctionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['seller','name','category']}),
    ]
    inlines = [BidderInline]

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ]



admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category, CategoryAdmin)