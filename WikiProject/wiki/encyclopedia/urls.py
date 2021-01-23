from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("edit/<str:entry>", views.editPage, name="editPage"),
    path("wiki", views.index, name="indexWiki"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newPage", views.newPage, name="newPage")
]