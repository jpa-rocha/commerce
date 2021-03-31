from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist/<str:itemid>", views.watchlist, name="watchlist"),
    path("categories/<str:cat>", views.categories, name="categories"),
    path('listing/<int:listnum>', views.listing, name='listing'),
    path('bids', views.bids, name='bids'),
    path('comments', views.comments, name='comments')
]
