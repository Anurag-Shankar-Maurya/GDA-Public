from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


from django.contrib.auth import logout
from django.contrib import messages


class OnboardingMiddleware:
    """
    Middleware to redirect users to onboarding if they haven't completed it.
    If a user has started onboarding but navigates away, they will be logged out.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of paths that should be excluded from the onboarding check
        excluded_paths = [
            reverse('onboarding'),
            reverse('account_logout'),
            reverse('login'),
        ]
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user needs onboarding
            user = request.user
            needs_onboarding = (
                not getattr(user, 'onboarding_complete', False) or
                not user.date_of_birth or
                not user.guardian_name or
                not user.guardian_relation or
                not user.address or
                not user.contact or
                not user.country_code
            )

            # Check if the current path should be excluded
            is_excluded_path = any(
                request.path.startswith(path) for path in excluded_paths
            ) or request.path.startswith(
                '/admin/'
            ) or request.path.startswith(
                '/static/'
            ) or request.path.startswith(
                '/media/'
            )

            if needs_onboarding and not is_excluded_path:
                # If user has visited onboarding but tries to navigate away, log them out
                if request.session.get('onboarding_visited', False):
                    logger.warning(
                        f"User {user.username} navigated away from onboarding. Logging out."
                    )
                    logout(request)
                    messages.warning(
                        request,
                        "You must complete your profile to continue. Please log in again to complete the onboarding process."
                    )
                    return redirect('login')
                
                # If user needs onboarding and hasn't visited yet, redirect them
                logger.info(f"Redirecting {user.username} to onboarding from {request.path}")
                return redirect('onboarding')

        response = self.get_response(request)
        return response