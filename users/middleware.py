"""
Custom middleware for handling OAuth and authentication errors.

This middleware captures authentication exceptions and renders a friendly
access_denied page instead of showing technical error messages to users.
"""

import logging
from django.shortcuts import render
from django.http import HttpResponse
from social_core.exceptions import AuthException, AuthForbidden

logger = logging.getLogger(__name__)


class OAuthErrorMiddleware:
    """
    Middleware to handle OAuth and authentication errors gracefully.
    
    Catches AuthException and related errors from social-auth and renders
    a user-friendly access_denied.html page instead of technical errors.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except (AuthException, AuthForbidden) as e:
            logger.warning(f"Authentication exception: {str(e)} (Path: {request.path})")
            return render(request, 'users/access_denied.html', status=403)
        except Exception as e:
            # Let other exceptions pass through
            raise
