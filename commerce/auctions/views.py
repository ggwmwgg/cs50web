from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Category, Listing, Bid, Comment, Watchlist



class NewListingForm(forms.Form):
    # Create fields: title, description, starting_bid, image_url (optionally), category (optionally)
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'id': 'title', 'name': 'title'})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={'rows': 5, 'class': "form-control", 'placeholder': "Enter a description for the listing"})
    )
    starting_bid = forms.DecimalField(
        label="Starting Bid",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting bid'}),
        min_value=0
    )
    image_url = forms.URLField(
        label="Image URL",
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter a URL for an image (optional)'}),
        required=False
    )
    category = forms.ModelChoiceField(
        label="Category",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

class AddCommentForm(forms.Form):
    comment = forms.CharField(
        label="Comment",
        widget=forms.Textarea(
            attrs={'rows': 5, 'class': "form-control", 'placeholder': "Leave a comment...", "style": "height: 50px;"})
    )

# class AddBidForm(forms.Form):
#     bid = forms.DecimalField(
#         label="Bid",
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter bid', "style": "display:inline-block;", "step": "0.1"}),
#         # getting last bid from bids to that listing and setting it as min value
#         #min_value=Listing.objects.last().bids.last().bid
#         # setting min value to listing starting bid from listing id in url
#         min_value=Listing.objects.get(id=listing_id).starting_bid
#     )





def index(request):
    # listings = Listing.objects.all()
    listings = Listing.objects.filter(is_active=True)
    listings = listings.order_by('-date')
    try:
        alert_message = request.GET["alert_message"]
        alert_type = request.GET["alert_type"]
    except:
        alert_message = None
        alert_type = None
    return render(request, "auctions/index.html", {
        "listings": listings,
        "alert_message": alert_message,
        "alert_type": alert_type
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
            alert_type = "alert-success"
            alert_message = "Logged in successfully!"
            return HttpResponseRedirect(
                reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    alert_type = "alert-dark"
    alert_message = "Logged out successfully!"
    return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)


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
            watch_list = Watchlist(user=user)
            watch_list.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        alert_type = "alert-success"
        alert_message = "Registered successfully!"
        return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create(request):
    user = request.user
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url,
                              category=category, user=user)
            listing.save()
            #return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            alert_type = "alert-success"
            alert_message = "Listing created successfully!"
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    else:
        form = NewListingForm()

    return render(request, "auctions/create.html", {'form': form})

def listing(request, listing_id):
    alert_type = "alert-danger"
    alert_message = "Listing not found."

    try:
        listing = Listing.objects.get(id=listing_id)

    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    # Updating listing current bid from last bid for that listing in bids
    try:
        listing.current_bid = listing.bids.last().bid
        listing.save()
    except AttributeError:
        pass
    is_owner = False
    if request.user.is_authenticated:
        user = request.user
        # Check if user owns listing
        if listing.user == user:
            is_owner = True
        else:
            is_owner = False
    else:
        user = None

    # Check if user added listing to watchlist
    in_watchlist = False
    if user is not None:
        try:
            watchlist = Watchlist.objects.filter(user=user, listing=listing)
        except Watchlist.DoesNotExist:
            watchlist = Watchlist(user=user)
            watchlist.save()
        if len(watchlist) > 0:
            in_watchlist = True
        else:
            in_watchlist = False

    bids = listing.listing_bids.all()
    comments = listing.listing_comments.all().order_by('-date')
    add_comment_form = AddCommentForm()
    min_value = 0
    if len(bids) > 0:
        min_value = bids.last().bid
    else:
        min_value = listing.starting_bid
    class AddBidForm(forms.Form):
        bid = forms.DecimalField(
            label="Bid",
            widget=forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': min_value, "style": "display:inline-block;"}),
            # getting last bid from bids to that listing and setting it as min value
            # min_value=Listing.objects.last().bids.last().bid
            # setting min value to listing starting bid from listing id in url
            min_value=min_value
        )
    add_bid_form = AddBidForm()

    try:
        alert_message = request.GET["alert_message"]
        alert_type = request.GET["alert_type"]
    except:
        alert_message = None
        alert_type = None

    won = False
    try:
        bids = listing.listing_bids.all().order_by('-date')
        first_bid = bids.first()
        if user == first_bid.user:
            won = True
    except AttributeError:
        won = False
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "alert_message": alert_message,
        "alert_type": alert_type,
        "is_owner": is_owner,
        "add_comment_form": add_comment_form,
        "in_watchlist": in_watchlist,
        "add_bid_form": add_bid_form,
        "bid": min_value,
        "won": won
    })

@login_required(login_url='/login')
def close(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        user = request.user
    except Listing.DoesNotExist:
        alert_type = "alert-danger"
        alert_message = "Listing not found."
        return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)

    if request.method == "POST":
        if user == listing.user:
            listing.is_active = False
            listing.save()
            alert_type = "alert-dark"
            alert_message = "Listing closed successfully!"
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
        else:
            alert_type = "alert-danger"
            alert_message = "You are not the owner of this listing."
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def add_comment(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        alert_type = "alert-danger"
        alert_message = "Listing not found."
        return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)

    if request.method == "POST":

        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            new_comment = Comment(comment=comment, user=request.user, listing=listing)
            new_comment.save()
            alert_type = "alert-success"
            alert_message = "Comment added successfully!"
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def watchlist(request):
    user = request.user
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        action_list = request.POST["action"]
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            alert_type = "alert-danger"
            alert_message = "Listing not found."
            return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)

        if user is not None:
            try:
                watch_list = Watchlist.objects.get(user=user)
            except Watchlist.DoesNotExist:
                watch_list = Watchlist(user=user)
                watch_list.save()
            wl_listings = watch_list.listing.all()
            alert_type = ""
            alert_message = ""

            if action_list == "r":
                if listing in wl_listings:
                    watch_list.listing.remove(listing)
                    watch_list.save()
                    alert_type = "alert-dark"
                    alert_message = "Listing removed from watchlist successfully!"
                else:
                    alert_type = "alert-danger"
                    alert_message = "Listing not found in watchlist."
                return HttpResponseRedirect(reverse("listing", args=(
                listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
            elif action_list == "a":
                if listing in wl_listings:
                    alert_type = "alert-danger"
                    alert_message = "Listing already in watchlist."
                else:
                    watch_list.listing.add(listing)
                    watch_list.save()
                    alert_type = "alert-success"
                    alert_message = "Listing added to watchlist successfully!"
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
            elif action_list == "remove":
                if listing in wl_listings:
                    watch_list.listing.remove(listing)
                    watch_list.save()
                    alert_type = "alert-dark"
                    alert_message = "Listing removed from watchlist successfully!"
                else:
                    alert_type = "alert-danger"
                    alert_message = "Listing not found in watchlist."
                return HttpResponseRedirect(reverse("watchlist") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    else:
        try:
            watchlist_t = Watchlist.objects.get(user=user)
        except Watchlist.DoesNotExist:
            watchlist_t = Watchlist(user=user)
            watchlist_t.save()
        listings = watchlist_t.listing.all()
        listings = listings.order_by('-date')

        empty = True
        if len(listings) > 0:
            empty = False

        try:
            alert_message = request.GET["alert_message"]
            alert_type = request.GET["alert_type"]
        except:
            alert_message = None
            alert_type = None
        return render(request, "auctions/watchlist.html", {
            "listings": listings,
            "alert_message": alert_message,
            "alert_type": alert_type,
            "empty": empty
        })

@login_required(login_url='/login')
def add_bid(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        alert_type = "alert-danger"
        alert_message = "Listing not found."
        return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)

    if request.method == "POST":
        bids = listing.listing_bids.all()
        min_value = 0
        if len(bids) > 0:
            min_value = bids.last().bid
        else:
            min_value = listing.starting_bid
        class AddBidForm(forms.Form):
            bid = forms.DecimalField(
                label="Bid",
                widget=forms.NumberInput(
                    attrs={'class': 'form-control', 'placeholder': min_value, "style": "display:inline-block;"}),
                # getting last bid from bids to that listing and setting it as min value
                # min_value=Listing.objects.last().bids.last().bid
                # setting min value to listing starting bid from listing id in url
                min_value=min_value
            )
        form = AddBidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            if len(bids) > 0:
                if bid > bids.last().bid:
                    new_bid = Bid(bid=bid, user=request.user, listing=listing)
                    listing.current_bid = bid
                    new_bid.save()
                    listing.save()
                    alert_type = "alert-success"
                    alert_message = "Bid added successfully!"
                    return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
                else:
                    alert_type = "alert-danger"
                    alert_message = "Bid must be higher than the current bid."
                    return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
            else:
                if bid > listing.starting_bid:
                    new_bid = Bid(bid=bid, user=request.user, listing=listing)
                    listing.current_bid = bid
                    new_bid.save()
                    listing.save()
                    alert_type = "alert-success"
                    alert_message = "Bid added successfully!"
                    return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
                else:
                    alert_type = "alert-danger"
                    alert_message = "Bid must be higher than the starting bid."
                    return HttpResponseRedirect(reverse("listing", args=(listing.id,)) + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        alert_type = "alert-danger"
        alert_message = "Category not found."
        return HttpResponseRedirect(reverse("index") + "?alert_message=" + alert_message + "&alert_type=" + alert_type)
    listings = Listing.objects.filter(category=category)
    listings = listings.order_by('-date')

    empty = True
    if len(listings) > 0:
        empty = False

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings,
        "empty": empty
    })