from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import widgets
from django.forms.models import modelformset_factory
from django.forms.widgets import  HiddenInput, NumberInput, Select, TextInput
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from .models import Listing, User


class NewListingForm(ModelForm):
    class Meta:
         
         model = Listing
         fields = ['name', 'description', 'price', 'picture', 'category']
         widgets = {
            'name': TextInput(attrs={'placeholder' : 'Your listing name'}),
            'description' : Textarea(attrs={'placeholder' : 'Short description of your item'}),
            'price' : NumberInput(attrs={'min' : '0.01', 'step' : 'any', 'placeholder' : '€'}),
            
        }
        



def index(request):
    return render(request, "auctions/index.html")


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
            print(request.FILES['picture'])
            user = request.user
            listing = Listing.objects.create(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
                                             price=form.cleaned_data['price'], picture=request.FILES['picture'],
                                             user=user)
            listing.category.set(form.cleaned_data['category'])
           
            return render(request, "auctions/index.html")
        else:
            print("NOT VALID")
            return render(request, "auctions/create.html",{
                "form" : form
            })
    else:
        user = request.user
        print(user.id)
        return render(request, "auctions/create.html",{
            "form" : NewListingForm()
        })
    
