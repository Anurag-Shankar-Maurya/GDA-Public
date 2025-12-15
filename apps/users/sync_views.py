"""
User sync API views for GDA
"""
import os
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .sync_utils import create_user_from_sync

logger = logging.getLogger(__name__)
User = get_user_model()


def validate_sync_api_key(request):
    """Validate the sync API key from request headers"""
    api_key = request.headers.get('X-Sync-API-Key')
    expected_key = os.getenv('KICC_API_KEY', 'gda-kicc-sync-key-2024-secure')
    return api_key == expected_key


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def sync_create_user(request):
    """
    Create a user in GDA from KICC sync data
    """
    # Validate API key
    if not validate_sync_api_key(request):
        return Response(
            {'error': 'Invalid sync API key'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        user_data = request.data
        email = user_data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user from sync data
        user, created, error = create_user_from_sync(user_data)
        
        if error:
            return Response(
                {'error': error},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if created:
            logger.info(f"Created user {email} from KICC sync")
            return Response(
                {
                    'message': 'User created successfully',
                    'user_id': user.id,
                    'email': user.email,
                    'created': True
                },
                status=status.HTTP_201_CREATED
            )
        else:
            logger.info(f"User {email} already exists in GDA")
            return Response(
                {
                    'message': 'User already exists',
                    'user_id': user.id,
                    'email': user.email,
                    'created': False
                },
                status=status.HTTP_409_CONFLICT
            )
    
    except Exception as e:
        logger.error(f"Error in sync_create_user: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def sync_check_user(request):
    """
    Check if a user exists in GDA
    """
    # Validate API key
    if not validate_sync_api_key(request):
        return Response(
            {'error': 'Invalid sync API key'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        email = request.GET.get('email')
        
        if not email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user exists
        user_exists = User.objects.filter(email=email).exists()
        
        return Response(
            {
                'exists': user_exists,
                'email': email
            },
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        logger.error(f"Error in sync_check_user: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def sync_health_check(request):
    """
    Health check endpoint for sync service
    """
    # Validate API key
    if not validate_sync_api_key(request):
        return Response(
            {'error': 'Invalid sync API key'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(
        {
            'status': 'healthy',
            'service': 'GDA User Sync',
            'version': '1.0'
        },
        status=status.HTTP_200_OK
    )