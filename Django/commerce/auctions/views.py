from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Category,Product,Comment,Bid

from datetime import datetime



"""
yapılanlar:
Backend;

-listings/<int:listing_id>
-listings/<int:listing_id>/comment
-index.html display.products().filter(active=1)

Frontend;

-listings.html  write.comment,display.comment,product
-index.html     for product in products,click product --> listings/<product_id>


-modeller değiştirildi-


"""

class NewProduct(forms.Form):
    pass

def index(request):
    products = Product.objects.filter(active=1)
    return render(request, "auctions/index.html",{
            "products" : products
    })

def listings(request,listing_id):
    product = Product.objects.get(pk=listing_id)
    comments = Comment.objects.filter(product=listing_id)
    bids = Bid.objects.filter(product=listing_id)
    owner = User.objects.get(pk=product.owner)
    return render(request,"auctions/listings.html",{
        "product" : product,
        "comments" : comments,
        "bids" : bids,
        "owner" : owner
    })

def comment(request,listing_id):
    if request.method == "POST":
        title = request.POST["title"]
        comment = request.POST["comment"]
        
        product = Product.objects.get(pk=listing_id)

        user = User.objects.get(pk=request.user.id)

        addComment = Comment(product=product,author=user,commentTitle=title,comment=comment)
        addComment.save()

        return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

def bid(request,listing_id):
    if request.method == "POST":
        bid = float(request.POST["bid"])
        
        product = Product.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        

        comments = Comment.objects.filter(product=listing_id)
        
        bids = Bid.objects.filter(product=listing_id)
        owner = User.objects.get(pk=product.owner)
        if bid <= float(product.Bid) or bid <= float(product.startingBid) :
            comments = Comment.objects.filter(product =listing_id)
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "warningmessage" :  "You can't offer a bid lower than the product's current price.",
                "owner" : owner

            })  
        elif user.id == product.seller.id:
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "warningmessage" :  "You can't offer a bid your product.",
                "owner" : owner
            }) 

        if user.id == product.owner :
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "warningmessage" :  "You can't offer a bid again.",
                "owner" : owner
            }) 

        else:
            addBid = Bid(buyer=user,product=product,bid=bid)
            addBid.save()
            product.Bid = bid
            product.save()
            product.owner = user.id
            product.save()
            owner = User.objects.get(pk=product.owner)
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "successmessage" :  "Succesfull !",
                "owner" : owner
            })    

def createlisting(request):
    pass

def categories(request):
    categories = Category.objects.all()
    return render(request,"auctions/categories.html",{
        "categories":categories
    })

def wishlist(request):
    pass


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
