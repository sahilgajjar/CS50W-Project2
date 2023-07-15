from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bids, Comments, Category
from .forms import ListingForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

def category(request):

    categories = Category.objects.values('category').distinct()

    if request.method == "POST":
        try:
            category = request.POST["category"]
            c1 = Category.objects.get(category=category)
            l1 = Listing.objects.filter(category=c1, is_active=True)
            #if the category is empty error will generate and make l1 false
        except : 
            c1 = None 
            l1 = False
    else:
        l1 = True
        c1 = None

    return render(request, "auctions/categories.html", {
        "categories": categories,
        "listings": l1,
        "current": c1 
    })
    
def watchlist(request):
 
    user = User.objects.get(username=request.user)
    listings = user.watchlist_user.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

# adding comments in page
def comments(request, listing_id):

    l1 = Listing.objects.get(id=listing_id) 
    
    if request.method == "POST":
        comment = request.POST['comment']
        c1 = Comments(comment=comment, user=request.user, listing=l1)
        c1.save() 

        request.method = "GET"
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

#check for the valid bid
def check_bid(placedbid, currentbid):
    if (currentbid >= placedbid):
        return False
    else:
        return True 

def close_listing(request, listing_id):

    l1 = Listing.objects.get(id=listing_id)
    l1.is_active = False
    l1.save()
    #TODO only show active listing in index page where l1.isActive() is True
    try:
        obj = Bids.objects.filter(listing=l1).latest("bid_amount")
        print(obj)

    except ObjectDoesNotExist:
        print("bid don't exist") 
        obj = None
    
    request.method = "GET"
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

# assume that listing is not in watchlist 
def add_to_watchlist(request, listing_id):
    
    l1 = Listing.objects.get(id=listing_id)
    user = User(username=request.user)

    l1.watchlist.add(request.user)

    request.method = "GET"
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

def remove_from_watchlist(request, listing_id):
    
    l1 = Listing.objects.get(id=listing_id)

    l1.watchlist.remove(request.user)

    request.method = "GET"
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

# weather the listing is in wathchlist or not
def check_watchlist(user, listing_id):
    
    l1 = Listing.objects.get(id=listing_id)

    if l1.watchlist.filter(id=user.id).exists():
        return True
    else:
        return False


def listing(request, listing_id):
    
    try: 
        l1 = Listing.objects.get(id=listing_id)
    except:
        return HttpResponse("Sorry! Page does not exist")

    comments = Comments.objects.filter(listing = l1)
    # get the latest bid
    try:
        obj = Bids.objects.filter(listing=l1).latest("bid_amount")
        print(obj)

    except ObjectDoesNotExist:
        print("bid don't exist") 
        obj = None

    # if the listing is not active 
    if l1.is_active == False:

        return render(request, "auctions/listing.html", {
            "listing" : l1,
            "watchlist": None,
            "bid": obj,
            "close": True,
            "comments": comments
        })    
    # for all other listing
    else:
        # mininmum amount for listing
        if l1.current_bid_amount:
            min = l1.current_bid_amount + 1
        else:
            min = l1.starting_bid_amount
        
        # for the post request
        if request.method == "POST":
            
            bid = request.POST['bid']

            if(l1.current_bid_amount):
                if(check_bid(int(bid), l1.current_bid_amount)):
                    # creating a new bid
                    b1 = Bids(listing=l1, user=request.user, bid_amount=int(bid))
                    b1.save()

                    l1.current_bid_amount = int(bid)
                    l1.save()
                    message = True
                else:
                    message = False
            else:
                if(int(bid) >= l1.starting_bid_amount):
                    b1 = Bids(listing=l1, user=request.user, bid_amount=int(bid))
                    b1.save()

                    l1.current_bid_amount = int(bid)
                    l1.save()
                    message = True
                else:
                    message = False

            return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

        # if not post request check for authenticated user
        if request.user.is_authenticated:
        
            if l1.owner == request.user:

                return render(request, "auctions/listing.html", {
                    "listing" : l1,
                    "watchlist": check_watchlist(request.user, listing_id),
                    "min_value": min,
                    "bid": obj,
                    "yours": True,
                    "comments": comments 
                })        

            return render(request, "auctions/listing.html", {
                "listing" : l1,
                "watchlist": check_watchlist(request.user, listing_id),
                "min_value": min,
                "bid": obj,
                "comments": comments
            })        
        else:
            return render(request, "auctions/listing.html", {
                "listing" : l1,
                "watchlist": None,
                "bid": obj
            })        

#creating listing with the data get from user
def create(request):

    if request.method == "POST":

        form = ListingForm(request.POST)
        content = request.POST
        c1 = content['category'] 
    
        try:
            category = Category.objects.get(category=c1)
        except Category.DoesNotExist:
            category = Category(category=c1)
            category.save()

        l = Listing(
            listing = content['title'],
            starting_bid_amount = content['starting_bid'],
            current_bid_amount = None, 
            description = content['description'],
            url = content['Image'], 
            owner = request.user,
            category = category
        )

        l.save()

    return render(request, "auctions/listing_form.html", {
        "form" : ListingForm()
    })

# displaying all the listing in the index page
def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
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
