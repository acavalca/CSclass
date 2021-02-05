from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:listingID>", views.listingsView, name="listingsView"),
    path("listings/<int:listingID>/user", views.listingsUserView, name="listingsUserView"),
    path("create", views.createListing, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
