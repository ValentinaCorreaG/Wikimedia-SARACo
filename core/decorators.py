"""
Permission decorators for SARA views.

Three user types:
  - SUPERUSER: Full CRUD (create, read, update, delete)
  - STAFF: Can create and read only
  - ANONYMOUS: Read only (must be authenticated)
"""
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


def permission_denied_response(request):
    """
    Handle access denied.
    
    For HTMX requests: Return 403 Forbidden
    For regular GET requests: Render access_denied.html page
    For other requests: Redirect back with error message
    """
    messages.error(request, _("No tienes permisos para realizar esta acción."))
    
    # For HTMX requests, return 403 (JavaScript will show toast)
    if request.headers.get('HX-Request'):
        return HttpResponseForbidden("No tienes permisos para esta acción.")
    
    # For GET requests, render access_denied page
    if request.method == 'GET':
        return render(request, 'users/access_denied.html', status=403)
    
    # For other requests, redirect back
    return redirect(request.META.get('HTTP_REFERER', '/'))


def require_superuser(view_func):
    """
    Decorator to require superuser permissions (superuser only).
    Use for: EDIT, DELETE operations (only administrators)
    
    Usage:
        @require_superuser
        def edit_event(request, pk):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return permission_denied_response(request)
        return view_func(request, *args, **kwargs)
    return wrapper


def require_superuser_or_staff(view_func):
    """
    Decorator to require superuser or staff permissions.
    Use for: CREATE operations (administrators and team members only)
    
    Usage:
        @require_superuser_or_staff
        def create_event(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return permission_denied_response(request)
        return view_func(request, *args, **kwargs)
    return wrapper


def require_staff_or_superuser(view_func):
    """
    Decorator to require staff or superuser permissions.
    Use for: Operations available to staff and superuser
    
    Usage:
        @require_staff_or_superuser
        def view_reports(request):
            ...
    """
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return permission_denied_response(request)
        return view_func(request, *args, **kwargs)
    return wrapper


def require_authenticated(view_func):
    """
    Decorator to require authenticated user (login required).
    Use for: READ operations and general viewing
    
    Usage:
        @require_authenticated
        def view_activity(request, pk):
            ...
    """
    return login_required(view_func)


def require_create_permission(view_func):
    """
    Decorator to require CREATE permission.
    SUPERUSER and STAFF can create.
    
    Usage:
        @require_create_permission
        def create_event(request):
            ...
    """
    return require_superuser_or_staff(view_func)


def require_edit_permission(view_func):
    """
    Decorator to require EDIT permission.
    Only SUPERUSER can edit.
    
    Usage:
        @require_edit_permission
        def edit_event(request, pk):
            ...
    """
    return require_superuser(view_func)


def require_delete_permission(view_func):
    """
    Decorator to require DELETE permission.
    Only SUPERUSER can delete.
    
    Usage:
        @require_delete_permission
        def delete_event(request, pk):
            ...
    """
    return require_superuser(view_func)

