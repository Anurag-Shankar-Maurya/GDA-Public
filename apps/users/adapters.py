from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to handle onboarding redirects after social login
    """

    def get_login_redirect_url(self, request):
        """
        Override login redirect to check for onboarding
        """
        user = request.user
        logger.info(f"CustomAccountAdapter: Checking redirect for user {user.username if user.is_authenticated else 'anonymous'}")

        if user.is_authenticated:
            # If the social flow set a session flag, honor it first (helps first-login case)
            try:
                session_needs = bool(request.session.get('needs_onboarding', False))
            except Exception:
                session_needs = False

            if session_needs:
                logger.info("CustomAccountAdapter: session requests onboarding redirect")
                # Clear session flag
                try:
                    if 'needs_onboarding' in request.session:
                        del request.session['needs_onboarding']
                except Exception:
                    pass
                return reverse('onboarding')

            # Check if user needs onboarding (either flag is False or required fields are empty)
            needs_onboarding = (
                not getattr(user, 'onboarding_complete', False) or
                not user.date_of_birth or
                not user.guardian_name or
                not user.guardian_relation or
                not user.address or
                not user.contact or
                not user.country_code
            )

            logger.info(f"CustomAccountAdapter: onboarding_complete={getattr(user, 'onboarding_complete', 'N/A')}, needs_onboarding={needs_onboarding}")

            if needs_onboarding:
                logger.info("CustomAccountAdapter: Redirecting to onboarding")
                return reverse('onboarding')

        # Fallback to default behavior (uses LOGIN_REDIRECT_URL or next param)
        logger.info("CustomAccountAdapter: Using default redirect")
        return super().get_login_redirect_url(request)