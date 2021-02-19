from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid, Comment, Watchlists, Category
from django.core.exceptions import MultipleObjectsReturned


def index(request):
    user = request.user
    if user.is_authenticated:
        if not Watchlists.objects.filter(user=request.user).exists():
            newWatchlist = Watchlists(user=request.user)
            newWatchlist.save()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isOpen=True)
    })

def watchlistView(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Watchlists.objects.get(user=request.user).listings.all()
    })
def categoriesView(request):
    return render(request, "auctions/categories.html", {
        "categoriesList": Category.objects.all(),
    })

def categoryView(request, categoryName):
    return render(request, "auctions/category.html", {
        "categoryName": categoryName,
        "listings": Category.objects.get(name=categoryName).listings.all(),
    })

def listingsView(request, listingID):
    currentListing = Listing.objects.get(pk=listingID)
    if currentListing.creator == request.user:
        isSameUser = True
    else:
        isSameUser = False
    if request.method == "POST":
        if request.POST.get("bidSubmit"):
            newBidPrice = request.POST["newBidPrice"]
            newBidCreator = request.user
            newBidListing = currentListing
            newBid = Bid(price=newBidPrice, creator=newBidCreator, listing=newBidListing)
            newBid.save()
        if request.POST.get("commentSubmit"):
            newCommentBody = request.POST["newComment"]
            newCommentCreator = request.user
            newCommentListing = currentListing
            newComment = Comment(body=newCommentBody, creator=newCommentCreator, listing=newCommentListing)
            newComment.save()
        if request.POST.get("openSubmit"):
            currentListing.isOpen = bool(request.POST["isOpenForm"])
            currentListing.save()
        if request.POST.get("watchlistSubmit"):
            w = Watchlists.objects.get(user=request.user)
            if bool(request.POST["placeOnWatchlist"]):
                w.listings.add(currentListing)
            else:
                w.listings.remove(currentListing)
    tieHappened = False
    if currentListing.bids.exists():
        highestBid = currentListing.price
        for bid in currentListing.bids.all():
            if highestBid <= bid.price:
                highestBid = bid.price
        try:
            test = currentListing.bids.get(price=highestBid)
            if test.creator == request.user:
                userIsWinning = True
            else:
                userIsWinning = False
        except MultipleObjectsReturned:
            tieHappened = True
            userIsWinning = False
            test = currentListing.bids.filter(price=highestBid).first()
        return render(request, "auctions/listing.html", {
            "listing": currentListing,
            "comments": currentListing.comments.all(),
            "highestBid": test,
            "minBid": highestBid+1,
            "userIsWinning": userIsWinning,
            "noBid": False,
            "isSameUser": isSameUser,
            "tieHappened": tieHappened,
        })
    return render(request, "auctions/listing.html", {
        "listing": currentListing,
        "comments": currentListing.comments.all(),
        "highestBid": currentListing.price,
        "minBid": currentListing.price+1,
        "userIsWinning": False,
        "noBid": True,
        "isSameUser": isSameUser,
        "tieHappened": tieHappened,
    })

def createListing(request):
    if request.method == "POST":
        #name = str(request.POST["whichCategory"])
        
        newListingName = request.POST["newListingName"]
        newListingPrice = request.POST["newListingPrice"]
        newListingBody = request.POST["newListingBody"]
        newListingImgURL = request.POST["newListingImgURL"]
        newListingUser = request.user
        newListing = Listing(name=newListingName, price=newListingPrice, body=newListingBody, creator=newListingUser, imageURL=newListingImgURL, isOpen=True)
        newListing.save()
        if bool(request.POST["whichCategory"]):
            c = Category.objects.get(name=request.POST["whichCategory"])
            c.listings.add(newListing)
        return HttpResponseRedirect(reverse("listingsView", args=[newListing.pk]))
    return render(request, "auctions/createListing.html", {
        "categoriesList": Category.objects.all(),
    })


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
