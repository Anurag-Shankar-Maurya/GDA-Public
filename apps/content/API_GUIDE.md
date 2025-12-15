# Content App API Guide

This guide documents the REST API endpoints provided by the Content app for managing projects, news/events, success stories, and FAQs.

## Base URL

All endpoints are prefixed with `/api/` as configured in the main router.

## Authentication

Most endpoints are publicly readable. Authentication may be required for write operations depending on your configuration.

## Endpoints

### Projects

#### List Projects
- **URL**: `/api/projects/`
- **Method**: GET
- **Description**: Retrieve a list of all projects
- **Query Parameters**:
  - `country`: Filter by country
  - `theme`: Filter by theme
  - `difficulty`: Filter by difficulty (Easy/Medium/Hard)
  - `is_featured`: Filter featured projects (true/false)
  - `is_active`: Filter active projects (true/false)
- **Response**: Array of Project objects

#### Get Project Details
- **URL**: `/api/projects/{id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific project
- **Response**: Single Project object

#### Create Project
- **URL**: `/api/projects/`
- **Method**: POST
- **Auth Required**: Yes
- **Description**: Create a new project
- **Body**: Project data (see Project Model below)

#### Update Project
- **URL**: `/api/projects/{id}/`
- **Method**: PUT/PATCH
- **Auth Required**: Yes
- **Description**: Update an existing project

#### Delete Project
- **URL**: `/api/projects/{id}/`
- **Method**: DELETE
- **Auth Required**: Yes
- **Description**: Delete a project

### News & Events

#### List News/Events
- **URL**: `/api/news-events/`
- **Method**: GET
- **Description**: Retrieve a list of news and events
- **Query Parameters**:
  - `content_type`: Filter by type (NEWS/EVENT/ANNOUNCEMENT)
  - `is_featured`: Filter featured items (true/false)
  - `is_published`: Filter published items (true/false)
- **Response**: Array of NewsEvent objects

#### Get News/Event Details
- **URL**: `/api/news-events/{id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific news/event

### Success Stories

#### List Success Stories
- **URL**: `/api/success-stories/`
- **Method**: GET
- **Description**: Retrieve a list of success stories
- **Query Parameters**:
  - `is_featured`: Filter featured stories (true/false)
  - `is_published`: Filter published stories (true/false)
  - `related_project`: Filter by related project ID
- **Response**: Array of SuccessStory objects

#### Get Success Story Details
- **URL**: `/api/success-stories/{id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific success story

### FAQs

#### List FAQs
- **URL**: `/api/faq/`
- **Method**: GET
- **Description**: Retrieve a list of FAQs ordered by display order
- **Response**: Array of FAQ objects

#### Get FAQ Details
- **URL**: `/api/faq/{id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific FAQ

## Data Models

### Project Model
```json
{
  "id": 1,
  "project_id": "project_id_1",
  "kicc_project_id": "external_id_123",
  "title": "Project Title",
  "teaser": "Brief description",
  "background_objectives": "Detailed objectives",
  "tasks_eligibility": "Tasks and eligibility criteria",
  "country": "Taiwan",
  "theme": "Education",
  "duration": 40,
  "difficulty": "Medium",
  "headcount": 5,
  "total_headcount": 20,
  "cover_image": "path/to/image.jpg",
  "cover_image_url": "https://example.com/image.jpg",
  "video_urls": ["https://youtube.com/watch?v=123"],
  "image_urls": ["https://example.com/image1.jpg"],
  "gallery_images_count": 3,
  "application_deadline": "2025-12-31T23:59:59Z",
  "start_date": "2025-01-01",
  "end_date": "2025-01-31",
  "is_active": true,
  "is_hero_highlight": false,
  "is_featured": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### NewsEvent Model
```json
{
  "id": 1,
  "news_event_id": "news_event_id_1",
  "title": "News Title",
  "body": "Full content",
  "content_type": "NEWS",
  "cover_image": "path/to/image.jpg",
  "cover_image_url": "https://example.com/image.jpg",
  "external_link": "https://external-site.com",
  "video_urls": ["https://youtube.com/watch?v=123"],
  "image_urls": ["https://example.com/image1.jpg"],
  "gallery_images_count": 2,
  "publish_date": "2025-01-01T00:00:00Z",
  "is_published": true,
  "is_hero_highlight": false,
  "is_featured": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### SuccessStory Model
```json
{
  "id": 1,
  "success_story_id": "success_story_id_1",
  "title": "Success Story Title",
  "body": "Full story content",
  "related_project": 1,
  "cover_image": "path/to/image.jpg",
  "cover_image_url": "https://example.com/image.jpg",
  "is_hero_highlight": false,
  "is_featured": true,
  "image_urls": ["https://example.com/image1.jpg"],
  "video_urls": ["https://youtube.com/watch?v=123"],
  "gallery_images_count": 5,
  "beneficiaries": 100,
  "total_hours_contributed": 500,
  "is_published": true,
  "published_at": "2025-01-01T00:00:00Z",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### FAQ Model
```json
{
  "id": 1,
  "faq_id": "faq_id_1",
  "question": "What is GDA?",
  "answer": "GDA stands for Google Developer Academy...",
  "order": 1,
  "is_schema_ready": true,
  "thumbs_up": 15,
  "thumbs_down": 2,
  "total_votes": 17,
  "helpfulness_ratio": 88.2,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

## Filtering and Searching

### Projects
- Filter by country, theme, difficulty
- Filter by featured/active status
- Example: `/api/projects/?country=Taiwan&is_featured=true`

### News & Events
- Filter by content type
- Filter by published/featured status
- Example: `/api/news-events/?content_type=NEWS&is_featured=true`

### Success Stories
- Filter by featured/published status
- Filter by related project
- Example: `/api/success-stories/?is_featured=true&related_project=1`

## Pagination

All list endpoints support pagination. Use the following query parameters:
- `page`: Page number
- `page_size`: Number of items per page (default: 10)

## Error Responses

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

API endpoints may have rate limiting applied. Please check the response headers for rate limit information.</content>
<parameter name="filePath">d:\PythonDev\Projects\GDA-Public\apps\content\API_GUIDE.md