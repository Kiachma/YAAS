__author__ = 'eaura'
from django.shortcuts import render
from Auctions.models import Category, Auction


def base(request,category_id):
    category_list = Category.objects.order_by('name')
    if category_id is None or category_id==u'None':
        latest_auction_list = Auction.objects.order_by('created')
    else:
        latest_auction_list = Auction.objects.filter(category=category_id).order_by('created')
    context = {'category_list': category_list,'latest_auction_list': latest_auction_list}
    return render(request, 'base.html', context)


