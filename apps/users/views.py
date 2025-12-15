from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, ResendVerificationForm, CustomUserProfileForm, CustomUserOnboardingForm
from .email_utils import send_verification_email as send_verification_email_html, send_password_reset_email
from .models import Certificate
import logging
from django.utils.safestring import mark_safe
from datetime import date
from apps.content.models import Project, NewsEvent, SuccessStory, FAQ, FAQVote
from django.db.models import Sum

User = get_user_model()
logger = logging.getLogger(__name__)


def send_verification_email(request, user):
	"""
	Helper function to send HTML verification email with proper error handling
	Returns: (success: bool, error_message: str or None)
	"""
	try:
		success, error = send_verification_email_html(request, user)
		if success:
			logger.info(f"Verification email sent successfully to {user.email}")
		else:
			logger.error(f"Failed to send verification email to {user.email}: {error}")
		return success, error
		
	except Exception as e:
		logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
		return False, str(e)


def register(request):
	if request.method == 'POST':
		form = CustomUserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False  # Require email verification
			user.save()
			
			# Send verification email with error handling
			success, error = send_verification_email(request, user)
			
			if success:
				messages.success(
					request, 
					'Registration successful! Please check your email to verify your account.'
				)
			else:
				# Check if it's a configuration error
				if error and ('Email configuration error' in str(error) or 'Authentication Required' in str(error)):
					messages.warning(
						request,
						'Your account has been created, but email service is currently not configured. '
						'Please contact the administrator to verify your account or set up email functionality.'
					)
				else:
					messages.warning(
						request,
						'Your account has been created, but we encountered an issue sending the verification email. '
						'Please use the "Resend Verification" option to receive your verification link.'
					)
			
			return redirect('login')
	else:
		form = CustomUserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})


def verify_email(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	
	if user and default_token_generator.check_token(user, token):
		user.email_verified = True
		user.is_active = True
		user.save()
		logger.info(f"Email verified successfully for user: {user.email}")
		messages.success(request, 'Email verified! You can now log in.')
		return redirect('login')
	else:
		logger.warning(f"Invalid or expired verification attempt for uidb64: {uidb64}")
		messages.error(
			request, 
			'Invalid or expired verification link. Please request a new verification email.'
		)
		return redirect('resend_verification')


def resend_verification(request):
	if request.method == 'POST':
		form = ResendVerificationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			try:
				user = User.objects.get(email=email)
				
				if not user.is_active:
					# Send verification email with error handling
					success, error = send_verification_email(request, user)
					
					if success:
						messages.success(
							request, 
							f'Verification email has been sent to {email}. Please check your inbox and spam folder.'
						)
					else:
						# Check if it's a configuration error
						if error and ('Email configuration error' in str(error) or 'Authentication Required' in str(error)):
							messages.error(
								request,
								'Email service is currently not configured. Please contact the administrator to set up email functionality.'
							)
						else:
							messages.error(
								request,
								'We encountered an issue sending the verification email. Please try again later or contact support if the problem persists.'
							)
				else:
					messages.info(request, 'Your email is already verified. You can log in now.')
					
			except User.DoesNotExist:
				# Don't reveal if email exists or not for security reasons
				messages.info(
					request, 
					'If an account exists with this email, a verification link has been sent.'
				)
				logger.warning(f"Verification resend attempted for non-existent email: {email}")
			
			return redirect('login')
	else:
		form = ResendVerificationForm()
	return render(request, 'users/resend_verification.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			logger.info(f"User logged in successfully: {user.email}")
			messages.success(request, f'Welcome back, {user.username}!')
			
			# Check if user needs onboarding
			needs_onboarding = (
				not getattr(user, 'onboarding_complete', False) or
				not user.date_of_birth or
				not user.guardian_name or
				not user.guardian_relation or
				not user.address or
				not user.contact or
				not user.country_code
			)
			
			if needs_onboarding:
				return redirect('onboarding')
			
			return redirect('profile')
		else:
			# If form is not valid, it means authentication failed.
			# We need to check if the user exists and if their email is verified
			# to provide a more specific error message.
			username_or_email = request.POST.get('username') # Assuming username field can also take email
			try:
				user = User.objects.get(email=username_or_email)
			except User.DoesNotExist:
				try:
					user = User.objects.get(username=username_or_email)
				except User.DoesNotExist:
					user = None

			if user:
				if not user.email_verified:
					logger.warning(f"Login attempt with unverified email: {user.email}")
					# Modified message for unverified email (consistent with the above block)
					messages.error(request,	mark_safe(f'Your email address is not verified. Please verify it to log in. <a href="{reverse("resend_verification")}" class="alert-link text-blue-500">Resend Verification Email</a>'))
					return render(request, 'users/login.html', {'form': form})
				else:
					# User exists and is active, but credentials are incorrect
					messages.error(request, 'Invalid username or password. Please try again.')
			else:
				# User does not exist
				messages.error(request, 'No account found with this username or email.')
			
			return render(request, 'users/login.html', {'form': form})
	else:
		form = CustomAuthenticationForm()
	return render(request, 'users/login.html', {'form': form})


def logout_view(request):
	user_email = request.user.email if request.user.is_authenticated else 'anonymous'
	logout(request)
	logger.info(f"User logged out: {user_email}")
	messages.success(request, 'You have been logged out successfully.')
	return redirect('login')


def forgot_password(request):
	if request.method == 'POST':
		form = CustomPasswordResetForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			logger.info(f"Password reset requested for email: {email}")

			# Check if user with this email exists
			try:
				user = User.objects.get(email=email)
				logger.info(f"User found: {user.username} for email: {email}")
				
				# Check if user's email is verified
				if not user.email_verified:
					logger.warning(f"Password reset attempted for unverified email: {email}")
					messages.error(
						request,
						mark_safe(f'Your email address ({email}) is not verified yet. '
						'You must verify your email before you can reset your password. '
						f'<a href="{reverse("resend_verification")}" class="alert-link">Click here to resend verification email</a>.')
					)
					return redirect('resend_verification')
				
				# User exists and is verified, proceed with HTML password reset email
				try:
					success, error = send_password_reset_email(
						user,
						use_https=request.is_secure(),
						request=request
					)
					if success:
						logger.info(f"Password reset email sent successfully to: {email}")
						messages.success(
							request, 
							f'Password reset link has been sent to {email}. Please check your inbox and spam folder.'
						)
					else:
						logger.error(f"Failed to send password reset email to {email}: {error}")
						# Check if it's a configuration error
						if error and ('Email configuration error' in str(error) or 'Authentication Required' in str(error)):
							messages.error(
								request,
								'Email service is currently not configured. Please contact the administrator to set up email functionality.'
							)
						else:
							messages.error(
								request, 
								'We encountered an issue sending the password reset email. Please try again later or contact support if the problem persists.'
							)
				except Exception as e:
					logger.error(f"Failed to send password reset email to {email}: {str(e)}")
					error_str = str(e)
					# Check if it's a configuration/authentication error
					if 'Email configuration error' in error_str or 'Authentication Required' in error_str or '530' in error_str:
						messages.error(
							request,
							'Email service is currently not configured. Please contact the administrator to set up email functionality.'
						)
					else:
						messages.error(
							request, 
							'We encountered an issue sending the password reset email. Please try again later or contact support if the problem persists.'
						)
				
				return redirect('login')
				
			except User.DoesNotExist:
				logger.warning(f"Password reset attempted for non-existent email: {email}")
				# User doesn't exist, add error to form
				form.add_error(
					'email', 
					'No account found with this email address. Please check your email or register for a new account.'
				)
	else:
		form = CustomPasswordResetForm()
	return render(request, 'users/forgot_password.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
	from django.contrib.auth.views import PasswordResetConfirmView
	view = PasswordResetConfirmView.as_view(
		template_name='users/password_reset_confirm.html',
		form_class=CustomSetPasswordForm,
		success_url=reverse('login')
	)
	return view(request, uidb64=uidb64, token=token)


from django.contrib.auth.decorators import login_required

# Social login signals
from allauth.socialaccount.signals import social_account_added, social_account_updated, pre_social_login
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@login_required
def profile(request):
	if not request.user.is_authenticated:
		messages.warning(request, 'Please log in to view your profile.')
		return redirect('login')
	
	# Get enrolled projects
	enrolled_projects = request.user.enrolled_projects.all()
	today = date.today()
	
	upcoming_projects = []
	current_projects = []
	past_projects = []
	
	for project in enrolled_projects:
		if project.start_date and project.start_date > today:
			upcoming_projects.append(project)
		elif project.end_date and project.start_date and project.start_date <= today <= project.end_date:
			current_projects.append(project)
		else:
			past_projects.append(project)
            
	# Certificates Logic
	certificates = Certificate.objects.filter(user=request.user)
	certificate_map = {cert.project_id: cert for cert in certificates}
	
	eligible_projects = []
	for project in past_projects:
		if project.id in certificate_map:
			project.user_certificate = certificate_map[project.id]
		else:
			project.user_certificate = None
			eligible_projects.append(project)
	
	# Additional data for dashboard
	recent_news_events = NewsEvent.objects.filter(is_published=True).order_by('-publish_date')[:5]
	success_stories = SuccessStory.objects.filter(is_published=True, related_project__in=enrolled_projects).order_by('-published_at')[:5]
	faqs = FAQ.objects.all().order_by('order')[:10]
	
	# Get user's votes for FAQs
	user_faq_votes = {vote.faq_id: vote.vote_type for vote in FAQVote.objects.filter(user=request.user, faq__in=faqs)}
	for faq in faqs:
		faq.user_vote = user_faq_votes.get(faq.id, None)
	
	# User impact metrics
	impact_data = SuccessStory.objects.filter(
		related_project__in=past_projects, 
		is_published=True
	).aggregate(
		total_beneficiaries=Sum('beneficiaries'),
		total_hours=Sum('total_hours_contributed')
	)
	total_beneficiaries = impact_data['total_beneficiaries'] or 0
	total_hours = impact_data['total_hours'] or 0
	
	# Form for Edit Profile tab
	form = CustomUserProfileForm(instance=request.user)

    # Social accounts for Account Management tab
	from allauth.socialaccount.models import SocialAccount
	social_accounts = SocialAccount.objects.filter(user=request.user)
	connected_providers = [account.provider for account in social_accounts]

	context = {
		'user': request.user,
		'upcoming_projects': upcoming_projects,
		'current_projects': current_projects,
		'past_projects': past_projects,
		'certificates': certificates,
		'eligible_projects': eligible_projects,
		'recent_news_events': recent_news_events,
		'success_stories': success_stories,
		'faqs': faqs,
		'total_beneficiaries': total_beneficiaries,
		'total_hours': total_hours,
		'form': form,
		'social_accounts': social_accounts,
		'connected_providers': connected_providers,
	}
	return render(request, 'users/profile.html', context)


@login_required
def generate_certificate(request, project_id):
	if request.method != 'POST':
		return redirect('profile')
		
	project = get_object_or_404(Project, pk=project_id)
	
	# Verify user enrolled and project ended
	if not project.enrolled_users.filter(id=request.user.id).exists():
		messages.error(request, "You are not enrolled in this project.")
		return redirect('profile')
		
	today = date.today()
	if not project.end_date or project.end_date > today:
		messages.error(request, "This project has not ended yet.")
		return redirect('profile')
		
	# Check if certificate already exists
	certificate, created = Certificate.objects.get_or_create(
		user=request.user,
		project=project
	)
	
	if created:
		messages.success(request, f"Certificate generated for {project.title}!")
	else:
		messages.info(request, f"Certificate for {project.title} already exists.")
		
	return redirect('profile')


@login_required
def view_certificate(request, certificate_id):
	certificate = get_object_or_404(Certificate, certificate_id=certificate_id)

	# Check permission
	if certificate.user != request.user and not request.user.is_staff:
		messages.error(request, "You do not have permission to view this certificate.")
		return redirect('profile')

	context = {
		'user': certificate.user,
		'project': certificate.project,
		'certificate_id': certificate.certificate_id,
		'issued_at': certificate.issued_at,
	}
	return render(request, 'users/certificate.html', context)


def verify_certificate(request):
	"""
	Public view to verify certificate by ID
	Anyone can access this page to check certificate validity
	"""
	certificate = None
	error_message = None

	if request.method == 'POST':
		certificate_id = request.POST.get('certificate_id', '').strip()
		if certificate_id:
			try:
				certificate = Certificate.objects.select_related('user', 'project').get(certificate_id=certificate_id)
			except Certificate.DoesNotExist:
				error_message = "Invalid certificate ID. Please check and try again."
		else:
			error_message = "Please enter a certificate ID."

	context = {
		'certificate': certificate,
		'error_message': error_message,
	}
	return render(request, 'users/verify_certificate.html', context)


def certificate_verification_url(request, certificate_id):
	"""
	Direct URL verification
	"""
	certificate = None
	error_message = None
	
	try:
		certificate = Certificate.objects.select_related('user', 'project').get(certificate_id=certificate_id)
	except Certificate.DoesNotExist:
		error_message = "Invalid certificate ID. Please check and try again."
		
	context = {
		'certificate': certificate,
		'error_message': error_message,
	}
	return render(request, 'users/verify_certificate.html', context)


@login_required
def account_management(request):
	"""
	View for managing connected accounts and email
	"""
	from allauth.socialaccount.models import SocialAccount

	social_accounts = SocialAccount.objects.filter(user=request.user)
	context = {
		'user': request.user,
		'social_accounts': social_accounts,
	}
	return render(request, 'users/account_management.html', context)


@login_required
def delete_account(request):
	"""
	View for account deletion
	"""
	if request.method == 'POST':
		# Check if user confirmed deletion
		confirmation = request.POST.get('confirm_delete', '')
		if confirmation == request.user.username:
			# Deactivate user instead of deleting (better for data integrity)
			user = request.user
			user.is_active = False
			user.save()
			logout(request)
			messages.success(request, 'Your account has been deactivated successfully.')
			return redirect('login')
		else:
			messages.error(request, 'Confirmation username does not match. Account not deleted.')

	return render(request, 'users/delete_account.html')


@login_required
def profile_edit(request):
	if request.method == 'POST':
		form = CustomUserProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile has been updated successfully.')
			return redirect('profile')
	else:
		form = CustomUserProfileForm(instance=request.user)
	return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def onboarding(request):
	"""
	Onboarding view for collecting additional user details after social login
	"""
	# Check if user actually needs onboarding
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
	
	# If user doesn't need onboarding, logout the user
	if not needs_onboarding:
		return redirect('profile')

	# Set a session flag to indicate the user has visited the onboarding page
	request.session['onboarding_visited'] = True
	
	if request.method == 'POST':
		form = CustomUserOnboardingForm(request.POST, instance=request.user)
		if form.is_valid():
			user = form.save(commit=False)
			user.onboarding_complete = True
			user.is_active = True
			user.save()
			messages.success(request, 'Welcome! Your profile has been set up successfully.')

			# Clear the session flag once onboarding is complete
			if 'onboarding_visited' in request.session:
				del request.session['onboarding_visited']

			return redirect('profile')
	else:
		form = CustomUserOnboardingForm(instance=request.user)
	
	return render(request, 'users/onboarding.html', {'form': form})


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Handle user login - check if onboarding is needed and redirect accordingly
    """
    logger.info(f"User logged in: {user.username}")
    
    # Check if user needs onboarding
    needs_onboarding = (
        not getattr(user, 'onboarding_complete', False) or
        not user.date_of_birth or
        not user.guardian_name or
        not user.guardian_relation or
        not user.address or
        not user.contact or
        not user.country_code
    )
    
    if needs_onboarding:
        logger.info(f"Redirecting {user.username} to onboarding")
        from django.shortcuts import redirect
        from django.urls import reverse
        request.session['_onboarding_redirect'] = True
        # We'll handle the redirect in middleware or by overriding the response


@receiver(pre_social_login)
def pre_social_login_handler(request, sociallogin, **kwargs):
	"""
	Run before social login is processed. Ensure the login_method and onboarding
	session flags are available immediately for the redirect flow.
	"""
	try:
		provider = sociallogin.account.provider
	except Exception:
		provider = None

	# Determine method value
	method = 'email'
	if provider in ('google', 'facebook', 'github'):
		method = provider

	# Set session value so the very next request (redirect) can read it
	try:
		request.session['login_method'] = method
		logger.info(f"pre_social_login: set session login_method={method}")
	except Exception:
		logger.debug("pre_social_login: could not set session login_method")

	# If the sociallogin provides a user instance, mark needs_onboarding if incomplete
	user = getattr(sociallogin, 'user', None)
	needs_onboarding = False
	if user is not None:
		needs_onboarding = (
			not getattr(user, 'onboarding_complete', False) or
			not getattr(user, 'date_of_birth', None) or
			not getattr(user, 'guardian_name', None) or
			not getattr(user, 'guardian_relation', None) or
			not getattr(user, 'address', None) or
			not getattr(user, 'contact', None) or
			not getattr(user, 'country_code', None)
		)

	if needs_onboarding:
		try:
			request.session['needs_onboarding'] = True
			logger.info("pre_social_login: set session needs_onboarding=True")
		except Exception:
			logger.debug("pre_social_login: could not set session needs_onboarding")


# Social login signal handlers
@receiver(social_account_added)
def social_account_added_handler(request, sociallogin, **kwargs):
	"""
	Handle social account addition - set login method and check onboarding
	"""
	user = sociallogin.user
	logger.info(f"Social account added signal: user={user.username}, provider={sociallogin.account.provider}")

	# Set login method based on provider
	provider = sociallogin.account.provider
	if provider == 'google':
		user.login_method = 'google'
	elif provider == 'facebook':
		user.login_method = 'facebook'
	elif provider == 'github':
		user.login_method = 'github'
	else:
		user.login_method = 'email'  # fallback

	# For social logins, email is verified by the provider
	user.email_verified = True
	user.is_active = True

	user.save()
	logger.info(f"Set login_method to {user.login_method} and email_verified=True for user {user.username}")

	# Check if onboarding is needed
	if not user.onboarding_complete:
		# Store that we need to redirect to onboarding after login
		request.session['needs_onboarding'] = True
		logger.info(f"Set needs_onboarding session flag for user {user.username}")

	# Also set the login method in the session so it is available immediately
	try:
		request.session['login_method'] = user.login_method
		logger.info(f"Set session login_method={user.login_method} for user {user.username}")
	except Exception:
		# If session is not available for some reason, continue silently
		logger.debug("Could not set session login_method")


@receiver(social_account_updated)
def social_account_updated_handler(request, sociallogin, **kwargs):
	"""
	Handle social account updates
	"""
	# Similar logic as above
	social_account_added_handler(request, sociallogin, **kwargs)
