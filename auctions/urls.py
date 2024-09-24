from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("closed-listing", views.closedListing, name="closed-listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<str:listing_id>", views.comment, name="comment"),
    path("bidding/<str:listing_id>", views.bidding, name="bidding"),
    path("listing/<str:listing_id>/", views.listing, name="listing"),
    path('listing/<int:listing_id>/add_to_watchlist/', views.addToWatchlist, name='addToWatchlist'),
    path("create-listing", views.createListing, name="create-listing"),
]
