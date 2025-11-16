from django.shortcuts import render, redirect
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
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, ResendVerificationForm, CustomUserProfileForm
from .email_utils import send_verification_email as send_verification_email_html, send_password_reset_email
import logging
from django.utils.safestring import mark_safe
from datetime import date
from apps.content.models import Project

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
			if not user.is_active:
				logger.warning(f"Login attempt with unverified email: {user.email}")
				# Modified message for unverified email
				messages.error(request,	mark_safe(f'Your email address is not verified. Please verify it to log in. <a href="{reverse("resend_verification")}" class="alert-link text-blue-500">Resend Verification Email</a>'))
				return render(request, 'users/login.html', {'form': form})
			else:
				login(request, user)
				logger.info(f"User logged in successfully: {user.email}")
				messages.success(request, f'Welcome back, {user.username}!')
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
				if not user.is_active:
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
				if not user.is_active:
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
	
	context = {
		'user': request.user,
		'upcoming_projects': upcoming_projects,
		'current_projects': current_projects,
		'past_projects': past_projects,
	}
	return render(request, 'users/profile.html', context)


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