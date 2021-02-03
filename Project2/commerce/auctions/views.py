from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid
from django.core.exceptions import MultipleObjectsReturned


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isOpen=True)
    })

def listingsView(request, listingID):
    if request.method == "POST":
        newBidPrice = request.POST["newBidPrice"]
        newBidCreator = request.user
        newBidListing = Listing.objects.get(pk=listingID)
        newBid = Bid(price=newBidPrice, creator=newBidCreator, listing=newBidListing)
        newBid.save()
    if Listing.objects.get(pk=listingID).creator == request.user:
        isSameUser = True
    else:
        isSameUser = False
    if Listing.objects.get(pk=listingID).bids.exists():
        highestBid = Listing.objects.get(pk=listingID).price
        for bid in Bid.objects.all():
            if highestBid <= bid.price:
                highestBid = bid.price
        if Bid.objects.get(price=highestBid).creator == request.user:
            userIsWinning = True
        else:
            userIsWinning = False
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listingID),
            "isSameUser": isSameUser,
            "highestBid": Bid.objects.get(price=highestBid),
            "minBid": highestBid+1,
            "userIsWinning": userIsWinning,
            "noBid": False,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listingID),
            "isSameUser": isSameUser,
            "highestBid": Listing.objects.get(pk=listingID).price,
            "minBid": Listing.objects.get(pk=listingID).price+1,
            "userIsWinning": False,
            "noBid": True,
        })

def createListing(request):
    if request.method == "POST":
        newListingName = request.POST["newListingName"]
        newListingPrice = request.POST["newListingPrice"]
        newListingBody = request.POST["newListingBody"]
        newListingImgURL = request.POST["newListingImgURL"]
        newListingUser = request.user
        newListing = Listing(name=newListingName, price=newListingPrice, body=newListingBody, creator=newListingUser, imageURL=newListingImgURL)
        newListing.save()
    return render(request, "auctions/createListing.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
