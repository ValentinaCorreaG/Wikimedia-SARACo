"""
Permission template tags for SARA.

This module provides simple, reusable template tags to check user permissions.
Three user types:
  - SUPERUSER: Full CRUD access (create, read, update, delete)
  - STAFF: Can create and read only (no edit/delete)
  - ANONYMOUS: Can read only (no create/edit/delete, must be logged in to view)
"""
from django import template

register = template.Library()


@register.simple_tag
def can_create(user):
    """
    Check if user can create records.
    SUPERUSER and STAFF can create.
    
    Usage: {% can_create request.user as can %} {% if can %}...{% endif %}
    """
    return user.is_superuser or user.is_staff


@register.simple_tag
def can_edit(user):
    """
    Check if user can edit records.
    Only SUPERUSER can edit.
    
    Usage: {% can_edit request.user as can %} {% if can %}...{% endif %}
    """
    return user.is_superuser


@register.simple_tag
def can_delete(user):
    """
    Check if user can delete records.
    Only SUPERUSER can delete.
    
    Usage: {% can_delete request.user as can %} {% if can %}...{% endif %}
    """
    return user.is_superuser


@register.simple_tag
def can_view(user):
    """
    Check if user can view records.
    All authenticated users can view. Requires login.
    
    Usage: {% can_view request.user as can %} {% if can %}...{% endif %}
    """
    return user.is_authenticated


@register.simple_tag
def user_role(user):
    """
    Get a human-readable role name for the user.
    
    Returns one of: 'Administrador', 'Equipo', 'Visitante'
    
    Usage: {% user_role request.user as role %} {{ role }}
    """
    if user.is_superuser:
        return "Administrador"
    elif user.is_staff:
        return "Equipo"
    elif user.is_authenticated:
        return "Visitante"
    else:
        return "Anónimo"
