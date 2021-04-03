from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import  CheckboxSelectMultiple, NumberInput, TextInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from .models import Bids, Category, Comments, Listing, User, Watchlist


class NewListingForm(ModelForm):
    class Meta:  
         model = Listing
         fields = ['name', 'description', 'price', 'picture', 'category']
         widgets = {
            'name': TextInput(attrs={'placeholder' : 'Your listing name'}),
            'description' : Textarea(attrs={'placeholder' : 'Short description of your item'}),
            'price' : NumberInput(attrs={'min' : '0.01', 'step' : 'any', 'placeholder' : '€'}),
            'category' : CheckboxSelectMultiple()
        }       


def index(request):
    user = request.user
    listings = Listing.objects.all
    catlinks = Listing.category.through.objects.all()
    categories = Category.objects.all
    watchlist = Watchlist.objects.all
    wlist = []
    inlist = Watchlist.objects.filter(user_id=user.id)
    for i in inlist:
        wlist.append(i.item.id)
    return render(request, "auctions/index.html", {
        'listings' : listings,
        'catlinks' : catlinks,
        'categories' : categories,
        'watchlist' : wlist
    })


def watchlist(request, itemid):
    watchlist = Watchlist.objects.all
    listings = Listing.objects.all
    catlinks = Listing.category.through.objects.all()
    categories = Category.objects.all
    user = request.user
    if itemid != " ":
        itemid = int(itemid)
        item = Listing.objects.get(pk=itemid)
        inlist = Watchlist.objects.filter(user_id=user.id, item_id = item)
        check = inlist.exists()
        if not check:
            addition = Watchlist.objects.create(user=user,item=item)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            deletion = Watchlist.objects.filter(user_id=user.id, item_id = item).delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "auctions/watchlist.html",{
            'watchlist' : watchlist,
            'listings' : listings,
            'catlinks' : catlinks,
            'categories' : categories,
        })


def categories(request, cat):
    watchlist = Watchlist.objects.all
    listings = Listing.objects.all
    catlinks = Listing.category.through.objects.all()
    categories = Category.objects.all
    if cat == 'list':
        catlist = 'catlist'
        return render(request,'auctions/categories.html',{
            'categories' : categories,
            'catlist' : catlist
        })
    else:
        cat = cat
        category = Category.objects.get(category=cat)
        incat = []
        for i in catlinks:
            if i.category_id == category.id:
                incat.append(i.listing_id)
        return render(request,'auctions/categories.html',{
            'watchlist' : watchlist,
            'listings' : listings,
            'catlinks' : catlinks,
            'categories' : categories,
            'incat' : incat,
            'cat' : cat
        })


def listing(request, listnum):
    listnum = listnum
    listitem = Listing.objects.get(pk=listnum)
    watchlist = Watchlist.objects.all
    listings = Listing.objects.all
    catlinks = Listing.category.through.objects.all()
    categories = Category.objects.all
    user = request.user
    wlist = []
    inlist = Watchlist.objects.filter(user_id=user.id)
    comments = Comments.objects.filter(item=listitem)
    step = 0.1
    price = int(listitem.price) + step
    for i in inlist:
        wlist.append(i.item.id)
    if request.method == 'POST':
        itemid = request.POST['item']
        item = Listing.objects.get(pk=itemid)
        item.closed = True
        item.save()
        return HttpResponseRedirect(reverse("index"))
        
    return render(request,'auctions/listing.html',{
        'watchlist' : wlist,
        'listings' : listings,
        'catlinks' : catlinks,
        'categories' : categories,
        'item' : listitem,
        'comments' : comments,
        'price' : price,
        'step' : step
    })


def bids(request):
    watchlist = Watchlist.objects.all
    listings = Listing.objects.all
    catlinks = Listing.category.through.objects.all()
    categories = Category.objects.all
    user = request.user
    if request.method == 'POST':  
        itemid = request.POST['item']
        bid = float(request.POST['bid'])
        item = Listing.objects.get(pk=itemid)
        currentprice = float(request.POST['price'])
        if bid > currentprice:
            newbid = Bids.objects.create(user=user, item=item, amount=bid)
            item.price = bid
            item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        bids = Bids.objects.filter(user=user)
        bidset = set()
        for bid in bids:
            print(bid.item.id)
            bidset.add(bid.item.id)
        print(bidset)
        # for bid in bids if:  bid.amount == bid.item.price bid.user gets green message else red
        return render(request, 'auctions/bids.html',{
            'bids' : bids,
            'bidset' : bidset,
            'watchlist' : watchlist,
            'listings' : listings,
            'catlinks' : catlinks,
            'categories' : categories,
        })  


def comments(request):
    comment = request.POST['comment']
    user = request.user
    itemid = request.POST['item']
    item = Listing.objects.get(pk=itemid)
    newcomment = Comments.objects.create(user=user, item=item, comment=comment)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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


def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            user = request.user
            listing = Listing.objects.create(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
                                             price=form.cleaned_data['price'], original_price=form.cleaned_data['price'], 
                                             picture=request.FILES['picture'], user=user)
            listing.category.set(form.cleaned_data['category'])
           
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html",{
                "form" : form
            })
    else:
        user = request.user
        return render(request, "auctions/create.html",{
            "form" : NewListingForm()
        })
    
