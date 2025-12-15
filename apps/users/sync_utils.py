"""
User synchronization utilities for GDA-KICC integration
"""
import os
import requests
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from typing import Dict, Optional, Tuple, Any

logger = logging.getLogger(__name__)
User = get_user_model()


class UserSyncManager:
    """Handles user synchronization between GDA and KICC"""
    
    def __init__(self):
        self.kicc_api_base = os.getenv('KICC_API_BASE_URL', 'https://kicc-backend-2nig.onrender.com')
        self.kicc_api_key = os.getenv('KICC_API_KEY', 'gda-kicc-sync-key-2024-secure')
        self.sync_enabled = os.getenv('ENABLE_USER_SYNC', 'True') == 'True'
        
    def is_sync_enabled(self) -> bool:
        """Check if user sync is enabled"""
        return self.sync_enabled
    
    def get_sync_headers(self) -> Dict[str, str]:
        """Get headers for sync API requests"""
        return {
            'Content-Type': 'application/json',
            'X-Sync-API-Key': self.kicc_api_key,
            'User-Agent': 'GDA-Sync/1.0'
        }
    
    def sync_user_to_kicc(self, user: Any) -> Tuple[bool, Optional[str]]:
        """
        Sync user from GDA to KICC
        Returns: (success: bool, error_message: Optional[str])
        """
        if not self.is_sync_enabled():
            logger.info("User sync is disabled")
            return True, None
        
        try:
            # Prepare user data for KICC
            user_data = {
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.contact,
                'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
                'membership_type': 'GENERAL',  # Default membership for KICC
                'source_platform': 'GDA'
            }
            
            # Make API request to KICC
            url = f"{self.kicc_api_base}/api/accounts/sync/create-user/"
            response = requests.post(
                url,
                json=user_data,
                headers=self.get_sync_headers(),
                timeout=10
            )
            
            if response.status_code == 201:
                logger.info(f"Successfully synced user {user.email} to KICC")
                return True, None
            elif response.status_code == 409:
                # User already exists in KICC
                logger.info(f"User {user.email} already exists in KICC")
                return True, None
            else:
                error_msg = f"KICC sync failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during KICC sync: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during KICC sync: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def check_user_exists_in_kicc(self, email: str) -> Tuple[bool, bool]:
        """
        Check if user exists in KICC
        Returns: (exists: bool, sync_success: bool)
        """
        if not self.is_sync_enabled():
            return False, True
        
        try:
            url = f"{self.kicc_api_base}/api/accounts/sync/check-user/"
            response = requests.get(
                url,
                params={'email': email},
                headers=self.get_sync_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('exists', False), True
            else:
                logger.error(f"Failed to check user in KICC: {response.status_code}")
                return False, False
                
        except Exception as e:
            logger.error(f"Error checking user in KICC: {str(e)}")
            return False, False


def sync_user_after_registration(user: Any) -> None:
    """
    Sync user to KICC after successful registration in GDA
    This function is called from user registration flow
    """
    if not user or not user.email:
        return
    
    sync_manager = UserSyncManager()
    success, error = sync_manager.sync_user_to_kicc(user)
    
    if not success and error:
        logger.warning(f"User sync failed for {user.email}: {error}")
        # Continue with registration even if sync fails
        # We don't want to break the user experience


def create_user_from_sync(user_data: Dict) -> Tuple[Optional[Any], bool, Optional[str]]:
    """
    Create a GDA user from KICC sync data
    Returns: (user: Optional[User], created: bool, error: Optional[str])
    """
    try:
        email = user_data.get('email')
        if not email:
            return None, False, "Email is required"
        
        # Check if user already exists
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            return existing_user, False, None
        
        # Parse date_of_birth if provided
        date_of_birth = None
        if user_data.get('date_of_birth'):
            try:
                from datetime import datetime
                date_of_birth = datetime.fromisoformat(user_data['date_of_birth']).date()
            except (ValueError, TypeError):
                logger.warning(f"Invalid date_of_birth format: {user_data.get('date_of_birth')}")
                date_of_birth = None
        
        # Create new user
        user = User.objects.create_user(
            username=user_data.get('username', email.split('@')[0]),
            email=email,
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            contact=user_data.get('phone', ''),
            date_of_birth=date_of_birth,
            login_method='email',
            onboarding_complete=False
        )
        
        # Set a random password (user will need to reset it)
        import secrets
        temp_password = secrets.token_urlsafe(32)
        user.set_password(temp_password)
        user.save()
        
        logger.info(f"Created GDA user from KICC sync: {email}")
        return user, True, None
        
    except Exception as e:
        error_msg = f"Error creating user from sync: {str(e)}"
        logger.error(error_msg)
        return None, False, error_msg