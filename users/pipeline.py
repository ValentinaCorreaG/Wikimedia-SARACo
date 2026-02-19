"""
Authentication pipeline for Wikimedia OAuth integration.

This module provides custom pipeline steps for social-auth-app-django
to handle Wikimedia authentication with intelligent user matching and logging.
"""

import logging
from typing import Dict, Any, Optional
from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()
logger = logging.getLogger(__name__)


def associate_by_wiki_handle(
    backend: Any,
    uid: str,
    user: Optional[User] = None,
    *args: Any,
    **kwargs: Any
) -> Dict[str, User]:
    """
    Authentication pipeline step that associates a login attempt with an
    existing User based on a Wikimedia username.

    If a user is already authenticated, it returns immediately.
    Otherwise, it attempts to match the external username against:
    1. UserProfile.professional_wiki_handle (case-insensitive)
    2. User.username (fallback)

    This prevents duplicate accounts and allows users to authenticate
    using their Wikimedia username even if their Django username differs
    (backward compatibility, from when the login was not made with OAuth)

    Args:
        backend: Authentication backend in use.
        uid: Unique identifier provided by the authentication backend.
        user (User, optional): Already authenticated user, if any.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments, expected to include
                  a 'details' dict containing a 'username' key.

    Returns:
        dict: {'user': User} if a matching user is found, otherwise an empty dict.
    """
    if user:
        logger.info(f"User already authenticated: {user.username}")
        return {'user': user}

    details = kwargs.get('details', {})
    wiki_username = details.get('username')

    if wiki_username:
        # Try to match by professional wiki handle
        profile = UserProfile.objects.filter(
            professional_wiki_handle__iexact=wiki_username
        ).select_related('user').first()
        
        if profile:
            logger.info(
                f"User matched by wiki handle: {wiki_username} -> {profile.user.username}"
            )
            return {'user': profile.user}

        # Fallback to username matching
        user_ = User.objects.filter(username=wiki_username).first()
        if user_:
            logger.info(
                f"User matched by username: {wiki_username}"
            )
            return {'user': user_}
        
        logger.info(f"New user will be created: {wiki_username}")
    else:
        logger.warning("No wiki username provided in authentication details")

    return {}


def get_username(
    strategy: Any,
    details: Dict[str, Any],
    user: Optional[User] = None,
    *args: Any,
    **kwargs: Any
) -> Dict[str, str]:
    """
    Determines the username to be used during authentication with conflict resolution.

    If the user already exists, their current username is preserved.
    Otherwise, the username is derived from the Wikimedia authentication details.
    If a conflict exists, appends a number to make it unique.

    Args:
        strategy: Authentication strategy in use.
        details (dict): Authentication details provided by the backend,
            expected to include a 'username' key.
        user (User, optional): Existing user, if already authenticated.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        dict: {'username': str} representing the resolved username.
    """
    if user:
        return {"username": user.username}
    
    base_username = details.get('username', 'user')
    username = base_username
    counter = 1
    
    # Handle username conflicts by appending numbers
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"
        counter += 1
        
    if username != base_username:
        logger.warning(
            f"Username conflict resolved: {base_username} -> {username}"
        )
    
    return {"username": username}


def log_authentication_success(
    backend: Any,
    user: User,
    response: Dict[str, Any],
    *args: Any,
    **kwargs: Any
) -> None:
    """
    Log successful authentication events for monitoring and security.

    Args:
        backend: Authentication backend in use.
        user: Authenticated user.
        response: Response from the OAuth provider.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.
    """
    logger.info(
        f"Successful authentication: user={user.username}, "
        f"backend={backend.name}, uid={response.get('id', 'unknown')}"
    )
