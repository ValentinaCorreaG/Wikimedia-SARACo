"""URL configuration for users app."""

from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    # Authentication
    path("login/", views.login_view, name="login"),
    path("login/oauth/", views.login_oauth, name="login_oauth"),
    path("logout/", views.logout_view, name="logout"),
    path("oauth/error/", views.oauth_error, name="oauth_error"),
    
    # Profile management
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
    path("profile/<str:username>/", views.profile_view, name="profile_detail"),
    path("list/", views.user_list_view, name="user_list"),
    path("<int:user_id>/delete/", views.user_delete_view, name="user_delete"),
]
