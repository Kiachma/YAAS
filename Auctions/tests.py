"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import unicodedata

from django.test import TestCase
from django.contrib.auth.models import User
from Auctions.models import *
from django.core.urlresolvers import reverse
import datetime


class SimpleTest(TestCase):
    fixtures = ['Users_views_testdata.json', 'Auctions_views_testdata.json']

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@testuser.com', 'testuser')

    def testCreateAuction(self):
        category = Category.objects.get(pk=1)
        # Create auction without authentication
        resp = self.client.post(reverse('auctions:edit', args=('None',)),
                                {'name': 'Testauction', 'category': category, 'description': 'Description',
                                 'deadline':
                                     datetime.datetime.now() + datetime.timedelta(days=4),
                                 'min_price': '20'})
        self.assertEqual(resp.status_code, 302)

        #Login
        self.client.login(username='testuser', password='testuser')
        count =Auction.objects.count()
        resp = self.client.post(reverse('auctions:edit', args=('None',)),
                                {'name': 'Testauction', 'category': category, 'description': 'Description',
                                 'deadline':
                                     datetime.datetime.now() + datetime.timedelta(days=4),
                                 'min_price': '20'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(count+1,Auction.objects.count())


