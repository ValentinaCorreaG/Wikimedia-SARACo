"""URL configuration for users app."""

from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    # Authentication
    path("login/", views.login_view, name="login"),
    path("login/oauth/", views.login_oauth, name="login_oauth"),
    path("logout/", views.logout_view, name="logout"),
    
    # Profile management
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:username>/", views.profile_view, name="profile_detail"),
    path("list/", views.user_list_view, name="user_list"),
]
