"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from Auctions.models import *


class CreateAuctionTest(TestCase):
    fixtures = ['Users_views_testdata.json', 'Auctions_views_testdata.json']
    category = None

    def setUp(self):
        self.user=CustomUser()
        self.user.username= 'testuser'
        self.user.email='testuser@testuser.com'
        self.user.set_password('testuser')
        self.user.language='sv'
        self.user.save()
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
        dt = datetime.datetime(2014, 12, 5, 6, 0)
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
        self.assertRedirects(resp, reverse('index', args={''}))
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
        self.user=CustomUser()
        self.user.username= 'testuser'
        self.user.email='testuser@testuser.com'
        self.user.set_password('testuser')
        self.user.language='sv'
        self.user.save()
        self.user2=CustomUser()
        self.user2.username= 'testuser2'
        self.user2.email='testuser2@testuser2.com'
        self.user2.set_password('testuser2')
        self.user2.language='sv'
        self.user2.save()
        self.auction = Auction.objects.get(pk=12)
        self.dueAuction = Auction.objects.get(pk=13)
        self.bid = 10000
        self.bid2 = 10000

    def testPlaceBidWithoutAuthentication(self):
        resp = self.client.post(reverse('auctions:bid', args=('12',)),
                                {'bid': self.bid, 'edited_version': self.auction.version})
        self.assertEqual(resp.status_code, 302)


    def testPlaceBidWithAuthenticationSuccesfully(self):
        #Login
        self.client.login(username='testuser', password='testuser')
        # Place bid
        prevCount = Bid.objects.count()
        print("Bid count before creating a new Bid: " + str(prevCount))
        resp = self.client.post(reverse('auctions:bid', args=('12',)),
                                {'bid': self.bid, 'edited_version': self.auction.version})
        self.failUnlessEqual(resp.status_code, 302)
        print("Bid count after creating a new Bid: " + str(Bid.objects.count()))
        self.assertEqual(prevCount + 1, Bid.objects.count())
        latestBid = Auction.objects.get(pk=12).getLatestBid()
        self.assertEqual(latestBid.bid, self.bid)
        self.assertEqual(latestBid.auction, self.auction)
        self.assertEqual(latestBid.user, self.user)

    def testPlaceBidWithAuthenticationUnSuccesfully(self):
        c2 = Client()
        c2.login(username='testuser2', password='testuser2')
        self.client.login(username='testuser', password='testuser')
        # Place normal bid

        resp = self.client.post(reverse('auctions:bid', args=('12',)),
                                {'bid': self.bid, 'edited_version': self.auction.version})
        self.failUnlessEqual(resp.status_code, 302)
        prevCount = Bid.objects.count()
        #Place to low bid
        print("Bid count before creating a new Bid: " + str(prevCount))
        resp = c2.post(reverse('auctions:bid', args=('12',)),
                                {'bid': self.bid, 'edited_version': self.auction.version})
        prevCount = Bid.objects.count()
        print("Bid count after trying to place to low bid: " + str(Bid.objects.count()))
        self.assertEqual(prevCount, Bid.objects.count())
        prevCount = Bid.objects.count()
        #Place bid on due auction
        print("Bid count before creating a new Bid: " + str(prevCount))
        resp = c2.post(reverse('auctions:bid', args=('13',)),
                                {'bid': self.bid, 'edited_version': self.dueAuction.version})

        print("Bid count after trying to place bid on due auction: " + str(Bid.objects.count()))
        self.assertEqual(prevCount, Bid.objects.count())


    def testBidConcurrency(self):
        print("BID CONCURRENCY START-----------------------------------------")
        #Login
        c1 = Client()
        c2 = Client()
        c1.login(username='testuser', password='testuser')
        c2.login(username='testuser2', password='testuser2')
        # Place normal bid
        dt = datetime.datetime(2014, 12, 5, 6, 0)

        #C1 creates a new auction
        prevCount = Auction.objects.count()
        resp = c1.post(reverse('auctions:save', args=('None',)),
                       {'name': 'Testauction', 'category': 1, 'description': 'Description',
                        'deadline': dt
                           ,
                        'min_price': 20})
        resp = c1.post(reverse('auctions:confirm'),
                                {'confirm': 'True'})
        #C2 gets on version of auction
        latestAuction = Auction.objects.latest('created')
        resp = c2.get(reverse('auctions:view', args=(latestAuction.id,)))

        #C1 updates the auction
        resp2 = c1.post(reverse('auctions:save', args=(latestAuction.id,)),
                        {'name': 'Testauction', 'category': 1, 'description': 'Description2',
                         'deadline': dt
                            ,
                         'min_price': 20})
        prevCount = Bid.objects.count()
        #C2 tries to bid on the old version

        resp = c2.post(reverse('auctions:bid', args=(latestAuction.id,)),
                                {'bid': self.bid, 'edited_version': resp.context['auction'].version})
        self.assertEqual(prevCount, Bid.objects.count())
        print("BID CONCURRENCY END-----------------------------------------")








