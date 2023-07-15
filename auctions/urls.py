from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("<int:listing_id>", views.listing, name="listing_page"),
    path("watchlist_add/<int:listing_id>/", views.add_to_watchlist, name="watchlist_add"),
    path("watchlist_remove/<int:listing_id>/",views.remove_from_watchlist, name="watchlist_remove"),
    path("close/<int:listing_id>/", views.close_listing, name="close"),
    path("comments/<int:listing_id>/", views.comments, name="comment")
]
