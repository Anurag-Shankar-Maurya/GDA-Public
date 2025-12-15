# Users App API Guide

This guide documents the REST API endpoints provided by the Users app for managing user accounts, authentication, and certificates.

## Base URL

All endpoints are prefixed with `/api/` as configured in the main router.

## Authentication

Most endpoints require authentication. User registration is open, but profile management requires login.

## Endpoints

### Users

#### User Registration
- **URL**: `/api/users/`
- **Method**: POST
- **Description**: Register a new user account
- **Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "blood_group": "O+",
    "guardian_name": "Jane Doe",
    "guardian_relation": "Parent",
    "address": "123 Main St, City, Country",
    "contact": "1234567890",
    "country_code": "+1"
  }
  ```
- **Response**: User object with authentication token

#### Get Current User Profile
- **URL**: `/api/users/me/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: Retrieve the current authenticated user's profile

#### List Users
- **URL**: `/api/users/`
- **Method**: GET
- **Auth Required**: Yes (Staff only)
- **Description**: List all users (admin/staff only)

#### Get User Details
- **URL**: `/api/users/{id}/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: Get details of a specific user (users can only access their own profile unless staff)

#### Update User Profile
- **URL**: `/api/users/{id}/`
- **Method**: PUT/PATCH
- **Auth Required**: Yes
- **Description**: Update user profile information

#### Change Password
- **URL**: `/api/users/{id}/change_password/`
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  ```json
  {
    "old_password": "currentpassword",
    "new_password": "newsecurepassword123",
    "new_password2": "newsecurepassword123"
  }
  ```

### Certificates

#### List Certificates
- **URL**: `/api/certificates/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: List certificates for the authenticated user (or all if staff)

#### Get Certificate Details
- **URL**: `/api/certificates/{id}/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: Get details of a specific certificate

#### Create Certificate
- **URL**: `/api/certificates/`
- **Method**: POST
- **Auth Required**: Yes (Staff/Admin)
- **Description**: Issue a new certificate for a user-project combination
- **Body**:
  ```json
  {
    "user": 1,
    "project": 1
  }
  ```

### Social Accounts

#### List Social Accounts
- **URL**: `/api/social-accounts/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: List connected social accounts for the authenticated user

#### Get Social Account Details
- **URL**: `/api/social-accounts/{id}/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: Get details of a specific social account connection

## Data Models

### User Model
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "gender": "Male",
  "blood_group": "O+",
  "guardian_name": "Jane Doe",
  "guardian_relation": "Parent",
  "address": "123 Main St, City, Country",
  "contact": "1234567890",
  "country_code": "+1",
  "login_method": "email",
  "onboarding_complete": true,
  "email_verified": true
}
```

### Certificate Model
```json
{
  "id": 1,
  "user": 1,
  "user_name": "John Doe",
  "project": 1,
  "project_title": "Community Garden Project",
  "issued_at": "2025-01-01T00:00:00Z",
  "certificate_id": "GDA2025-ABC123"
}
```

### Social Account Model
```json
{
  "id": 1,
  "provider": "google",
  "provider_name": "Google",
  "provider_id": "google",
  "uid": "123456789012345678901",
  "date_joined": "2025-01-01T00:00:00Z",
  "last_login": "2025-01-01T00:00:00Z"
}
```

## Authentication Methods

The system supports multiple login methods:
- **Email/Password**: Standard authentication
- **Google**: OAuth with Google
- **Facebook**: OAuth with Facebook
- **GitHub**: OAuth with GitHub

### Social Login Endpoints

Social authentication is handled through django-allauth and provides the following endpoints:

#### Google Login
- **URL**: `/accounts/google/login/`
- **Method**: GET (redirects to Google OAuth)
- **Description**: Initiates Google OAuth login flow

#### Facebook Login
- **URL**: `/accounts/facebook/login/`
- **Method**: GET (redirects to Facebook OAuth)
- **Description**: Initiates Facebook OAuth login flow

#### GitHub Login
- **URL**: `/accounts/github/login/`
- **Method**: GET (redirects to GitHub OAuth)
- **Description**: Initiates GitHub OAuth login flow

#### Social Account Connections
- **URL**: `/accounts/social/connections/`
- **Method**: GET/POST
- **Auth Required**: Yes
- **Description**: View and manage connected social accounts

### Social Login Flow

1. User clicks social login button on login page
2. User is redirected to provider (Google/Facebook/GitHub)
3. User grants permissions
4. Provider redirects back with authorization code
5. System exchanges code for access token
6. User profile is created/updated with social account data
7. User is logged in and redirected based on onboarding status

## User Permissions

- **Regular Users**: Can view and edit their own profile, view their certificates
- **Staff Users**: Can view all users and certificates, manage content
- **Admin Users**: Full system access

## Validation Rules

### Password Requirements
- Minimum length: 8 characters
- Must contain at least one uppercase letter
- Must contain at least one lowercase letter
- Must contain at least one digit
- Must contain at least one special character

### Email Verification
- Email verification is required for account activation
- `email_verified` field tracks verification status

### Onboarding
- `onboarding_complete` tracks whether user has completed initial setup
- May be required before accessing certain features

## Error Responses

- `400 Bad Request`: Invalid data or validation errors
- `401 Unauthorized`: Authentication required or invalid credentials
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User or certificate not found
- `409 Conflict`: Duplicate certificate for user-project pair

## Rate Limiting

API endpoints may have rate limiting applied, especially for:
- User registration
- Password change attempts
- Certificate creation

## Security Features

- Password hashing using Django's secure hashing
- JWT token-based authentication (if implemented)
- CSRF protection
- SQL injection prevention through ORM
- XSS protection through template escaping</content>
<parameter name="filePath">d:\PythonDev\Projects\GDA-Public\apps\users\API_GUIDE.md