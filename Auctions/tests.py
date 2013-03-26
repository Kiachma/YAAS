"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


from Auctions.models import *


class CreateAuctionTest(TestCase):
    fixtures = ['Users_views_testdata.json', 'Auctions_views_testdata.json']
    category=None
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@testuser.com', 'testuser')
        self.category = Category.objects.get(pk=1)

    def testCreateAuctionWithoutAuthentication(self):
        resp = self.client.post(reverse('auctions:save', args=('None',)),
                                {'name': 'Testauction', 'category': 1, 'description': 'Description',
                                 'deadline':
                                     datetime.datetime.now() + datetime.timedelta(days=4),
                                 'min_price': 20})
        self.assertEqual(resp.status_code, 302)


    def testCreateAuctionWithAuthentication(self):
        current_tz = timezone.get_current_timezone()
        #Login
        self.client.login(username='testuser', password='testuser')
        dt =datetime.datetime(2014, 12, 5, 6, 0)
        # Create auction with authentication
        prevCount = Auction.objects.count()
        print("Auction count before creating a new auction: " + str(prevCount))
        resp = self.client.post(reverse('auctions:save', args=('None',)),
                                {'name': 'Testauction', 'category': 1, 'description': 'Description',
                                 'deadline': dt
                                     ,
                                 'min_price': 20})

        self.failUnlessEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "auctions/confirm.html")

        #Test confirm = False
        resp = self.client.post(reverse('auctions:confirm'),
                                {'confirm': 'False'})
        self.failUnlessEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('index',args={''}))
        self.assertEqual(prevCount, Auction.objects.count())

        #Test confirm = True
        resp = self.client.post(reverse('auctions:confirm'),
                                {'confirm': 'True'})
        self.failUnlessEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'auctions/view.html')
        print("Auction count after creating a new auction: " + str(Auction.objects.count()))
        self.assertEqual(prevCount + 1, Auction.objects.count())
        latestAuction = Auction.objects.latest('created')
        self.assertEqual(latestAuction.name, 'Testauction')
        self.assertEqual(latestAuction.category.id, self.category.id)
        self.assertEqual(latestAuction.description, 'Description')
        self.assertEqual(latestAuction.seller, self.user)


        self.assertEqual(latestAuction.min_price, 20)

class PlaceBidTest(TestCase):
    fixtures = ['Users_views_testdata.json', 'Auctions_views_testdata.json']
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@testuser.com', 'testuser')
        self.auction=Auction.objects.get(pk=13)
        self.amount=10000
        self.amount2=10000

    def testPlaceBidWithoutAuthentication(self):
        resp = self.client.post(reverse('auctions:bid', args=('13',)),
                                {  'bid': self.amount,})
        self.assertEqual(resp.status_code, 302)


    def testPlaceBidWithAuthenticationSuccesfully(self):
        #Login
        self.client.login(username='testuser', password='testuser')
        # Create auction with authentication
        prevCount = Bid.objects.count()
        print("Bid count before creating a new auction: " + str(prevCount))
        resp = self.client.post(reverse('auctions:bid', args=('13',)),
                                {'bid': self.amount,})
        self.failUnlessEqual(resp.status_code, 302)
        print("Bid count after creating a new auction: " + str(Bid.objects.count()))
        self.assertEqual(prevCount + 1, Bid.objects.count())
        latestBid = Auction.objects.get(pk=13).getLatestBid()
        self.assertEqual(latestBid.bid, self.amount)
        self.assertEqual(latestBid.auction, self.auction)
        self.assertEqual(latestBid.user, self.user)

    def testPlaceBidWithAuthenticationUnSuccesfully(self):
        #Login
        self.client.login(username='testuser', password='testuser')
        # Create auction with authentication
        prevCount = Bid.objects.count()
        print("Bid count before creating a new auction: " + str(prevCount))
        resp = self.client.post(reverse('auctions:bid', args=('13',)),
                                {'bid': self.amount,})
        self.failUnlessEqual(resp.status_code, 302)
        print("Bid count after creating a new auction: " + str(Bid.objects.count()))
        self.assertEqual(prevCount + 1, Bid.objects.count())
        latestBid = Auction.objects.get(pk=13).getLatestBid()
        self.assertEqual(latestBid.bid, self.amount)
        self.assertEqual(latestBid.auction, self.auction)
        self.assertEqual(latestBid.user, self.user)







