from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
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
    username = forms.CharField(label='Username')

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
            'country_code': forms.TextInput(attrs={
                'placeholder': 'e.g., +91',
            }),
        }
