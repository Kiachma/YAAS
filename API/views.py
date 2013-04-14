# Create your views here.

from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from Auctions.models import  *
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth.models import User
from YAAS.views import *
from django.utils import timezone
from datetime import timedelta

def apisearch(request, query):
    if query is None:
        auctions= Auction.objects.all()
    else:
        category_list, auctions = getAuctionBySearch(query)
    try:
        #xml = serializers.serialize("xml", [auction])
        #response = HttpResponse(xml, mimetype="application/xml")

        json =serializers.serialize("json", auctions)
        response = HttpResponse(json, mimetype="application/json")
        response.status_code = 200
    except (ValueError, TypeError, IndexError):
        response = HttpResponse()
        response.status_code = 400
        #	return response
    return response



class AuctionBid:

    def __call__(self, request, username,auction_id,amount):
        self.request = request
        self.auction_id = auction_id
        self.amount = amount
        # Look up the user and throw a 404 if it doesn't exist
        self.user = get_object_or_404(User, username=username)
        if not request.method in ["POST"]:
            return HttpResponseNotAllowed(["POST"])
            # Check and store HTTP basic authentication, even for methods that
        # don't require authorization.
        self.authenticate()
        # Call the request method handle
        if request.method=="POST":
            return self.bid()


    def authenticate(self):
        # Pull the auth info out of the Authorization: header
        auth_info = self.request.META.get("HTTP_AUTHORIZATION", None)
        #print self.request
        print auth_info
        if auth_info and auth_info.startswith("Basic "):
            basic_info = auth_info.split(" ", 1)[1]
            print basic_info, basic_info.decode("base64")
            u, p = basic_info.decode("base64").split(":")
            print u, p
            self.user = u
            # Authenticate against the User database. This will set
            # authenticated_user to None if authentication fails.
            self.authenticated_user = authenticate(username=u, password=p)
            print "self.authenticated_user,", self.authenticated_user
        else:
            self.authenticated_user = None

    def forbidden(self):
        response = HttpResponseForbidden()
        response["WWW-Authenticate"] = 'Basic realm="Auction"'
        return response


    def bid(self):
    # Check authorization
    #  print self.user, type(self.user), type(self.authenticated_user), self.authenticated_user
        if self.user != str(self.authenticated_user):
            print "forbidden"
            return self.forbidden()
            # Look up the bookmark...
        auction = get_object_or_404(Auction,  id=self.auction_id)
        bid=Bid()
        bid.auction=auction
        bid.user=self.authenticated_user
        bid.bid=int(self.amount)
        if auction.getLatestBidSum() >= bid.bid:
            response = HttpResponse()
            response.status_code = 409
        elif auction.seller==self.authenticated_user:
            response = HttpResponse()
            response.status_code = 409
        else:
            bid.save()
            try:
            #xml = serializers.serialize("xml", [auction])
            #response = HttpResponse(xml, mimetype="application/xml")
                json =serializers.serialize("json", [bid])
                response = HttpResponse(json, mimetype="application/json")
                response.status_code = 200
            except (ValueError, TypeError, IndexError):
                response = HttpResponse()
                response.status_code = 400
            if auction.deadline - timezone.now() < timedelta(minutes=5):
                auction.deadline += timedelta(minutes=5)
            auction.save()
        return response

        # Return a 204 ("no content")




def bid(request,auction_id,amount):
    a=Auction.objects.get(pk=auction_id)
    bid=Bid()
    bid.bid=amount
    bid.auction=a
    bid.user=request.user
    bid.save()
    try:
        #xml = serializers.serialize("xml", [auction])
        #response = HttpResponse(xml, mimetype="application/xml")

        json =serializers.serialize("json", [a])
        response = HttpResponse(json, mimetype="application/json")
        response.status_code = 200
    except (ValueError, TypeError, IndexError):
        response = HttpResponse()
        response.status_code = 400
        #	return response
    return response