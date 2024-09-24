from decimal import Decimal
from django.db.models import Max
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import OuterRef, Exists, Subquery

from auctions.models import Bid, Comment, Listing, User, WatchList

CATEGORY_CHOICES = [
        ('ELE', 'Electronics'),
        ('FAS', 'Fashion'),
        ('HOM', 'Home'),
        ('TOY', 'Toys'),
        ('ART', 'Art'),
        ('INS', 'Musical Instruments'),
    ]

CATEGORY_DICT={
    'ELE': 'Electronics',
    'FAS': 'Fashion',
    'HOM': 'Home',
    'TOY': 'Toys',
    'ART': 'Art',
    'INS': 'Musical Instruments'
}

class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    shortdesc = forms.CharField(max_length=120)
    desc = forms.CharField(widget=forms.Textarea, max_length=400)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    active = forms.BooleanField(initial=True,required=False)
    image = forms.URLField(max_length=500, required=False) 

def index(request):
    listings = Listing.objects.filter(active=True).order_by('-id')
    # if user logged in add watchlist parameter
    if request.user.is_authenticated:
        user = request.user
        # Defining a subquery to check if the listing is in the user's watchlist
        watchlist_subquery = WatchList.objects.filter(user=user, listing=OuterRef('pk'))

        # Annotate the listings with a boolean field 'in_watchlist'
        listings = listings.annotate(
            in_watchlist=Exists(watchlist_subquery)
        )
    return render(request, "auctions/index.html",{"listings":listings,"title":'Active Listing',"page":'active-listing'})

def closedListing(request):
    listings = Listing.objects.filter(active=False).order_by('-id')
    # if user logged in add watchlist parameter
    if request.user.is_authenticated:
        user = request.user
        # Defining a subquery to check if the listing is in the user's watchlist
        watchlist_subquery = WatchList.objects.filter(user=user, listing=OuterRef('pk'))

        # Annotate the listings with a boolean field 'in_watchlist'
        listings = listings.annotate(
            in_watchlist=Exists(watchlist_subquery)
        )
    return render(request, "auctions/index.html",{"listings":listings,"title":'Closed Listing',"page":'closed-listing'})

# List all categories
def categories(request):
    return render(request, "auctions/categories.html", {
        'categoryList': CATEGORY_CHOICES,"page":'categories'
    })


# Items within the specified category
def category(request, category):
    # Filter all items which belongs to the category
    listings = Listing.objects.filter(category=category,active=True).order_by('-id')
    
    return render(request, "auctions/categories.html", {
        'listings': listings, 'category': CATEGORY_DICT[category],"page":'category'
    })

@login_required
def watchlist(request):
    user = request.user
    
    # Define a subquery to check if the listing is in the user's watchlist
    watchlist_subquery = WatchList.objects.filter(user=user, listing=OuterRef('pk'))
    
    # Fetch only listings that are in the user's watchlist
    listings = Listing.objects.annotate(in_watchlist=Exists(watchlist_subquery)).filter(in_watchlist=True).order_by('-id')
    
    return render(request, "auctions/index.html", {"listings": listings, "title": "My Watchlist","page":'watchlist'})

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
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createListing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)

        # Validate form data
        if form.is_valid():
            data = form.cleaned_data
            print(f"data: {data}\n")

            # Create the listing if the form is valid
            listing = Listing.objects.create(
                title=data['title'],
                shortdesc=data['shortdesc'],
                desc=data['desc'],
                price=data['price'], 
                category=data['category'],
                active=data['active'],
                image=data['image'],
                listedBy=request.user  # Assuming the user is logged in
            )
            print(f"Listing created: {listing}")

            # Redirect to avoid resubmission when the page is refreshed
            return redirect('index')

        else:
            # If the form is not valid, print the errors
            print(form.errors)

    # Render the form template with the form instance
    return render(request, "auctions/create-listing.html")

def getListingData(request,listing_id,messageType,message):
    try:
        listing = Listing.objects.get(id=listing_id)
        # Attempt to retrieve the listing by its ID
        comments = Comment.objects.filter(listing=listing)
        biddings= Bid.objects.filter(listing=listing).order_by("-amount")[:5]

        highest_bid=biddings[0] if biddings else None
        currentPrice=highest_bid.amount if highest_bid else listing.price
        watchlist_item=None
        if request.user.is_authenticated:
            user=request.user
            watchlist_item = WatchList.objects.filter(user=user, listing=listing).first()
        data={
            "listing": listing,
            "comments": comments,
            "biddings":biddings,
            "highestBidder":highest_bid.user if highest_bid else None,
            "currentPrice":currentPrice,
            "inWatchlist":True if watchlist_item else False,
            "messageType":messageType,
            "message":message,
        }
        return data
    except Listing.DoesNotExist:
        # If the listing does not exist, pass an error message
        message="No such Listing. Please try again!!"
        data={
            "messageType":messageType,
            "message":message,
        }
        return data

def listing(request,listing_id):
    try:
        message=""
        if not request.user.is_authenticated:
            message="Please log in to bid and post comments for this listing"

        data=getListingData(request,listing_id,messageType="alert",message=message)
        return render(request, 'auctions/listing.html', data)
    except Listing.DoesNotExist:
        # If the listing does not exist, pass an error message
        message="No such Listing. Please try again!!"
        return render(request, 'auctions/listing.html', data)
    


@login_required
def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = get_object_or_404(Listing, id=listing_id)
        content = request.POST.get("comment", "").strip()  # Used get to avoid KeyError
        
        if not content:
            message = "Comment is empty. Please have some mercy!!"
            data=getListingData(request,listing_id,messageType="error",message=message)

            return render(request, 'auctions/listing.html', data)

        # Create the comment
        Comment.objects.create(user=user, listing=listing, content=content)
        return redirect('listing', listing_id)

    return redirect('index')

@login_required
def bidding(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        user = request.user
        
        if 'bid' in request.POST:
            amount = Decimal(request.POST.get('bid'))
            maxBid = Bid.objects.filter(listing=listing).aggregate(Max('amount'))['amount__max'] or listing.price
            
            # Validate the bid amount
            if amount <= maxBid or not listing.active:
                message = "Bidding price must be greater than the current price!"
                data = getListingData(request, listing_id=listing_id, messageType='error', message=message)
                return render(request, 'auctions/listing.html', data)
            
            # Create the bid
            Bid.objects.create(user=user, listing=listing, amount=amount)
            return redirect('listing', listing_id) 

        # Toggle item activity
        elif 'active' in request.POST:
            listing.active = not listing.active
            listing.save()
            return redirect('listing', listing_id)

    return redirect('index')


@login_required
def addToWatchlist(request,listing_id):
    if request.method == "POST":
        try:
            # data = json.loads(request.body.decode('utf-8'))
            # listing_id = data.get('listing_id')
            user = request.user
            listing = get_object_or_404(Listing, id=listing_id)
            
            # Check if the listing is already in the user's watchlist
            watchlist_item, created = WatchList.objects.get_or_create(user=user, listing=listing)
            
            if created:
                message = "Successfully added to watchlist"
            else:
                # If it's already in the watchlist, remove it
                watchlist_item.delete()
                message = "Successfully removed from watchlist"
            
            return JsonResponse({"success": True, "message": message}, status=200)

        # except json.JSONDecodeError:
        #     return JsonResponse({"success": False, "message": "Invalid request data"}, status=400)

        except IntegrityError:
            return JsonResponse({"success": False, "message": "Database error occurred. Please try again."}, status=500)

        except Exception as e:
            # Generic error handling, in case of unforeseen issues
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"}, status=500)

    # If it's not a POST request, redirect to the index page
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

