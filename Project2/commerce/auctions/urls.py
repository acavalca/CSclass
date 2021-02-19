from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:listingID>", views.listingsView, name="listingsView"),
    path("watchlist", views.watchlistView, name="watchlistView"),
    path("categories", views.categoriesView, name="categoriesView"),
    path("categories/<str:categoryName>", views.categoryView, name="categoryView"),
    path("create", views.createListing, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
