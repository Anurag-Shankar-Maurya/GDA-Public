from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Certificate
from allauth.socialaccount.models import SocialAccount

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                 'date_of_birth', 'gender', 'blood_group', 'guardian_name',
                 'guardian_relation', 'address', 'contact', 'country_code',
                 'login_method', 'onboarding_complete', 'email_verified')
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name',
                 'date_of_birth', 'gender', 'blood_group', 'guardian_name',
                 'guardian_relation', 'address', 'contact', 'country_code')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs

class CertificateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = Certificate
        fields = ('id', 'user', 'user_name', 'project', 'project_title', 
                 'issued_at', 'certificate_id')
        read_only_fields = ('id', 'issued_at', 'certificate_id')

class SocialAccountSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='get_provider_display', read_only=True)
    provider_id = serializers.CharField(source='provider', read_only=True)
    
    class Meta:
        model = SocialAccount
        fields = ('id', 'provider', 'provider_name', 'provider_id', 'uid', 
                 'date_joined', 'last_login')
        read_only_fields = ('id', 'provider', 'uid', 'date_joined', 'last_login')