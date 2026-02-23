"""
User authentication and profile management views.

This module provides views for OAuth login/logout and user profile management
with HTMX support for modern, interactive UI.
"""

import json
import logging
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from users.forms import UserCreationByRoleForm

User = get_user_model()
logger = logging.getLogger(__name__)


def login_view(request):
    """
    Display the login page with OAuth options.
    
    If user is already authenticated, redirect to home.
    For HTMX requests, return a partial template.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        Rendered login page or redirect.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    template = 'users/partials/login_form.html' if request.htmx else 'users/login.html'
    return render(request, template)


def login_oauth(request):
    """
    Initiate OAuth login using the MediaWiki backend.

    This view redirects the user to the social-auth login flow configured
    for the ``mediawiki`` backend.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirect to the OAuth provider login URL.
    """
    logger.info(f"OAuth login initiated from IP: {request.META.get('REMOTE_ADDR')}")
    messages.info(request, _("Redirecting to Wikimedia login..."))
    return redirect(reverse("social:begin", kwargs={"backend": "mediawiki"}))


def logout_view(request):
    """
    Log out the current user and redirect to the home page.

    This view clears the authenticated session using Django's ``logout``
    function and displays a success message.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirect to the home page.
    """
    username = request.user.username if request.user.is_authenticated else "Unknown"
    logout(request)
    logger.info(f"User logged out: {username}")
    messages.success(request, _("You have been logged out successfully."))
    return redirect('base')


@login_required
def profile_view(request, username=None):
    """
    Display a user's profile details.
    
    If no username is provided, show the current user's profile.
    Supports HTMX for partial page updates.

    Args:
        request: The HTTP request object.
        username: Username of the profile to display (optional).

    Returns:
        Rendered profile page.
    """
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    can_edit = request.user == user or request.user.is_staff
    
    context = {
        'profile_user': user,
        'can_edit': can_edit,
    }
    
    template = 'users/partials/profile_detail.html' if request.htmx else 'users/profile.html'
    return render(request, template, context)


@login_required
@permission_required("auth.view_user", raise_exception=True)
def user_list_view(request):
    """
    Display a list of all users.
    
    Requires view_user permission.
    Supports HTMX for dynamic loading.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered user list page.
    """
    create_user_form = UserCreationByRoleForm() if request.user.is_superuser else None

    if request.method == "POST":
        if not request.user.is_superuser:
            raise PermissionDenied

        create_user_form = UserCreationByRoleForm(request.POST)
        if create_user_form.is_valid():
            created_user = create_user_form.save()
            messages.success(request, _("User '%(username)s' was created successfully.") % {"username": created_user.username})
            
            if request.htmx:
                users = User.objects.select_related('profile').order_by('-is_staff', 'username')
                response = render(request, 'users/partials/user_table.html', {'users': users, 'can_edit': request.user.is_staff})
                response['HX-Retarget'] = '#user-list-content'
                response['HX-Reswap'] = 'innerHTML'
                response['HX-Trigger'] = json.dumps({
                    'modalClose': {
                        'modalId': 'create_user_modal',
                        'resetForm': True,
                        'formId': 'create-user-form'
                    }
                })
                return response
            return redirect("users:user_list")
        else:
            # Form validation failed
            if request.htmx:
                response = render(request, 'users/partials/user_create_form.html', {'create_user_form': create_user_form})
                response['HX-Trigger'] = json.dumps({
                    'formInvalid': {
                        'modalId': 'create_user_modal'
                    }
                })
                return response

    users = User.objects.select_related('profile').order_by('-is_staff', 'username')
    
    context = {
        'users': users,
        'can_edit': request.user.is_staff,
        'create_user_form': create_user_form,
    }
    
    template = 'users/partials/user_table.html' if request.htmx else 'users/user_list.html'
    return render(request, template, context)


@login_required
@require_http_methods(["DELETE"])
def user_delete_view(request, user_id):
    """
    Delete a user account.
    
    Only superusers can delete users, and they cannot delete themselves.
    Supports HTMX for dynamic table updates.

    Args:
        request: The HTTP request object.
        user_id: ID of the user to delete.

    Returns:
        Rendered user table partial or redirect.
    """
    if not request.user.is_superuser:
        raise PermissionDenied
    
    user_to_delete = get_object_or_404(User, id=user_id)
    
    if user_to_delete == request.user:
        messages.error(request, _("You cannot delete your own account."))
        if request.htmx:
            users = User.objects.select_related('profile').order_by('-is_staff', 'username')
            return render(request, 'users/partials/user_table.html', {'users': users})
        return redirect("users:user_list")
    
    username = user_to_delete.username
    user_to_delete.delete()
    
    logger.info(f"User '{username}' was deleted by '{request.user.username}'")
    messages.success(request, _("User '%(username)s' was deleted successfully.") % {"username": username})
    
    if request.htmx:
        users = User.objects.select_related('profile').order_by('-is_staff', 'username')
        return render(request, 'users/partials/user_table.html', {'users': users})
    
    return redirect("users:user_list")
