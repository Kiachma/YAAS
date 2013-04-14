__author__ = 'eaura'
from Auctions.models import *
import random
import datetime
from django.db import transaction
from django.conf import settings


class Populator:
    def addUser(self, num):
        user = CustomUser()
        user.last_name = 'LastName' + str(num)
        user.first_name = 'FirstName' + str(num)
        user.email = 'email' + str(num) + '@test.com'
        user.username = 'test' + str(num)
        user.set_password('test' + str(num))
        code,x=map(list, zip(*settings.LANGUAGES))
        user.language=supported = random.choice(code)
        user.save()


    def addAuction(self, num):
        auction = Auction()
        self.flush_transaction()
        Category.objects.filter()
        auction.category = Category.objects.get(name='Category' + str(random.randint(1, 10)))
        auction.name = 'AuctionName' + str(num)
        auction.deadline = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 5))
        auction.seller= CustomUser.objects.get(username='test' + str(random.randint(1, 50)))
        auction.min_price=50
        auction.description='Description'
        auction.status = AuctionStatus.active
        auction.save()

    def addCategory(self, num):
        cat = Category()
        cat.name = 'Category' + str(num)
        cat.save()


    def addBid(self, num):
        bid = Bid()
        self.flush_transaction()
        bid.auction = Auction.objects.get(name='AuctionName' + str(random.randint(1, num)))
        bid.user = CustomUser.objects.get(username='test' + str(random.randint(1, 50)))
        bid.bid = random.randint(50, 1000)
        bid.save()


    def populate(self):
        for num in range(1, 11):
            self.addCategory(num)

        for num in range(1, 51):
            self.addUser(num)
        for num in range(1, 51):
            self.addAuction(num)
            for bidnum in range(1, 3):
                self.addBid(num)


    @transaction.commit_manually
    def flush_transaction(self):
        transaction.commit()
