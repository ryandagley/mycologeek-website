# Mycologeek Website

A website dedicated to mycology and technology, featuring a blog system with categorized posts about mushrooms and tech topics.

## Features

- Responsive blog layout with featured posts
- Category system (Mushroom and Tech categories)
- Tag-based navigation
- Trending posts section
- Dynamic content loading via API
- Weather monitoring system
- Sensor data integration
- Google Analytics integration

## Technical Stack

- Python 3.x with Flask framework
- HTML5
- CSS3 (Bootstrap framework)
- JavaScript (Vanilla JS)
- AWS Services:
  - S3 for content storage
  - DynamoDB for post metadata
  - Secrets Manager for API keys
  - API Gateway
- Google Fonts integration
- Font Awesome icons

## Prerequisites
- Python 3.x
- pip (Python package installer)
- AWS account with appropriate permissions
- Required AWS services configured:
  - S3 bucket
  - DynamoDB table
  - AWS Secrets Manager

## Setup Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Install Dependencies
```pip install -r requirements.txt```

## Set Environment Variables
### AWS Configuration
```
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-west-2"
```

### Application Configuration
export FLASK_APP=app.py
export FLASK_ENV=development  # Use 'production' for production environment

### AWS Resource Requirements
- S3 Bucket named 'mycologeek'

- DynamoDB table 'mg-BlogPosts' with primary key 'PostID'

- AWS Secrets Manager entries for:

  - weatherAPIKey

  - cred-keys

### API Integration
The site requires configuration of the following environment variables:

- BLOG_API_ENDPOINT: The URL of the blog API endpoint

## Running the Application
### Start the Flask development server
```python app.py```

The application will be available at http://localhost:8080

## Development Notes
- The application uses Flask's development server by default

- For production deployment, use a production-grade WSGI server

- Ensure all AWS services are properly configured before running

- Weather monitoring system requires valid API keys

- Sensor data integration requires proper S3 bucket configuration

