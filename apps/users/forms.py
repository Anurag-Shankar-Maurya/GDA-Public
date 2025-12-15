from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group', 'guardian_name', 'guardian_relation', 'address', 'contact', 'country_code')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def confirm_login_allowed(self, user):
        if not user.is_active:
            if not getattr(user, 'email_verified', False):
                raise ValidationError(
                    self.error_messages["inactive"],
                    code="inactive",
                )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254)

class CustomSetPasswordForm(SetPasswordForm):
    pass

class ResendVerificationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary',
            'placeholder': 'you@example.com'
        })
    )

class CustomUserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'YYYY-MM-DD'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group', 'guardian_name', 'guardian_relation', 'address', 'contact', 'country_code')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name',
            }),
            'gender': forms.Select(attrs={
                'class': 'select-field',
            }),
            'blood_group': forms.Select(attrs={
                'class': 'select-field',
            }),
            'guardian_name': forms.TextInput(attrs={
                'placeholder': 'Enter guardian\'s full name',
            }),
            'guardian_relation': forms.TextInput(attrs={
                'placeholder': 'e.g., Father, Mother, Guardian',
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter your full address',
                'rows': 3,
            }),
            'contact': forms.TextInput(attrs={
                'placeholder': 'Enter phone number',
            }),
            'country_code': forms.Select(attrs={
                'class': 'select-field emoji-font',
            }),
        }

class CustomUserOnboardingForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group', 'guardian_name', 'guardian_relation', 'address', 'contact', 'country_code')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
                'placeholder': 'Enter your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
                'placeholder': 'Enter your last name',
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
            }),
            'blood_group': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
                'placeholder': 'Enter guardian\'s full name',
            }),
            'guardian_relation': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
                'placeholder': 'e.g., Father, Mother, Guardian',
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
                'placeholder': 'Enter your full address',
                'rows': 3,
            }),
            'contact': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-blue focus:border-primary-blue',
                'placeholder': 'Enter phone number',
            }),
            'country_code': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-blue focus:border-primary-blue emoji-font',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['guardian_name'].required = True
        self.fields['guardian_relation'].required = True
        self.fields['address'].required = True
        self.fields['contact'].required = True
        self.fields['country_code'].required = True
