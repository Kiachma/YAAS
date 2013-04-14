__author__ = 'eaura'
import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django import http
from django.utils.http import is_safe_url
from django.conf import settings
from django.utils.translation import check_for_language
from datetime import datetime
from YAAS import DBFixture
from Auctions.models import Category, Auction


def base(request, category_id):
    category_list = Category.objects.order_by('name')
    if category_id is None or category_id == u'None' or category_id == '':
        latest_auction_list = Auction.objects.filter(~Q(banned=True) & Q(status=0) & Q(deadline__gte=datetime.now())).order_by('created')
    else:
        latest_auction_list = Auction.objects.filter(Q(category=category_id) & ~Q(banned=True) & Q(status=0)).order_by(
            'created')
    context = {'category_list': category_list, 'latest_auction_list': latest_auction_list}
    return render(request, 'base.html', context)


def getAuctionBySearch(query_string):
    entry_query = get_query(query_string, ['name', ])
    latest_auction_list = Auction.objects.filter(entry_query & ~Q(banned=True)).order_by('created')
    category_list = Category.objects.order_by('name')
    return category_list, latest_auction_list


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        category_list, latest_auction_list = getAuctionBySearch(query_string)
    else:
        latest_auction_list = Auction.objects.order_by('created')
        category_list = Category.objects.order_by('name')
    context = {'category_list': category_list, 'latest_auction_list': latest_auction_list}

    return render(request, 'base.html', context)


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def populateDb(request):
    pop = DBFixture.Populator()
    pop.populate()
    return HttpResponseRedirect(reverse('index', args=('',)))


def changeLanguage(request):
    next = request.REQUEST.get('next')
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response