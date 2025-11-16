# GDA API Documentation

This document provides information about the GDA (Google Developer Academy) API endpoints and their usage.

## Authentication

The API uses token-based authentication for protected endpoints. For read-only operations, authentication is not required.

## Base URL

```
https://your-domain.com/api/
```

## Available Endpoints

### Users

#### User Registration
- **URL**: `/api/users/`
- **Method**: POST
- **Description**: Register a new user
- **Body**:
  ```json
  {
    "username": "username",
    "email": "user@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "blood_group": "O+",
    "guardian_name": "Jane Doe",
    "guardian_relation": "Parent",
    "address": "123 Street, City",
    "contact": "1234567890",
    "country_code": "+1"
  }
  ```

#### Get Current User Profile
- **URL**: `/api/users/me/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: Returns the profile of the currently authenticated user

#### Update User Profile
- **URL**: `/api/users/{id}/`
- **Method**: PUT/PATCH
- **Auth Required**: Yes
- **Description**: Update user profile information
- **Note**: Users can only update their own profile unless they are staff

#### Change Password
- **URL**: `/api/users/{id}/change_password/`
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  ```json
  {
    "old_password": "currentpassword",
    "new_password": "newpassword123",
    "new_password2": "newpassword123"
  }
  ```

### Projects

#### List Projects
- **URL**: `/api/projects/`
- **Method**: GET
- **Description**: Returns a paginated list of all projects
- **Parameters**:
  - `page`: Page number for pagination
  - `page_size`: Number of items per page (default: 10)

#### Get Single Project
- **URL**: `/api/projects/{id}/`
- **Method**: GET
- **Description**: Returns details of a specific project

#### Create Project
- **URL**: `/api/projects/`
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  ```json
  {
    "title": "Project Title",
    "description": "Project Description",
    "cover_image": "file",
    "difficulty": "BEGINNER",
    "is_featured": false
  }
  ```

### News & Events

#### List News & Events
- **URL**: `/api/news-events/`
- **Method**: GET
- **Description**: Returns a paginated list of all News & Events

#### Get Single News/Event
- **URL**: `/api/news-events/{id}/`
- **Method**: GET
- **Description**: Returns details of a specific news/event

#### Create News/Event
- **URL**: `/api/news-events/`
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  ```json
  {
    "title": "Event Title",
    "description": "Event Description",
    "cover_image": "file",
    "event_date": "2025-10-31",
    "is_hero_highlight": false,
    "is_featured": false
  }
  ```

### Success Stories

#### List Success Stories
- **URL**: `/api/success-stories/`
- **Method**: GET
- **Description**: Returns a paginated list of all success stories

#### Get Single Success Story
- **URL**: `/api/success-stories/{id}/`
- **Method**: GET
- **Description**: Returns details of a specific success story

#### Create Success Story
- **URL**: `/api/success-stories/`
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  ```json
  {
    "title": "Success Story Title",
    "description": "Success Story Description",
    "cover_image": "file"
  }
  ```

## Interactive Documentation

Interactive API documentation is available at:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Response Format

All responses are returned in JSON format. Paginated responses follow this structure:

```json
{
  "count": 100,
  "next": "http://api.example.org/accounts/?page=2",
  "previous": null,
  "results": [
    // Data objects
  ]
}
```

## Error Handling

The API uses conventional HTTP response codes:
- 2xx for successful operations
- 4xx for client errors
- 5xx for server errors

Error responses include a message explaining the error:

```json
{
  "error": "Detailed error message"
}
```