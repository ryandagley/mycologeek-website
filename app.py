from flask import Flask, render_template, abort
import os
from weather import get_weather_data, get_api_key, get_weather_history_from_dynamodb, get_secrets, get_sensor_data
from datetime import datetime
import markdown
import boto3
import pytz

# Define the app variable as Flask
app = Flask(__name__)

# Pacific Time Zone (Tacoma)
pacific_tz = pytz.timezone('US/Pacific')

# AWS S3 Setup
S3_BUCKET = 'mycologeek'
s3_client = boto3.client('s3')

# AWS DynamoDB Setup
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('mg-BlogPosts')

def fetch_post_from_s3(bucket, key):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        post_content = response['Body'].read().decode('utf-8')
        return post_content
    except Exception as e:
        print(f"Error fetching post from S3: {e}")
        return None

# Routes to the templates

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/archive.html')
def archive():
    return render_template('archive.html')

@app.route('/about-ryan.html')
def about_ryan():
    return render_template('about-ryan.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/disclaimer.html')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/faq.html')
def faq():
    return render_template('faq.html')

@app.route('/gallery.html')
def gallery():
    return render_template('gallery.html')

@app.route('/monitor.html')
def monitor():
    city_name = 'Tacoma'
    secret_name = 'weatherAPIKey'
    api_key = get_api_key(secret_name)
    temperature = get_weather_data(city_name, api_key)

    # Fetch historical weather data from DynamoDB
    historical_weather = get_weather_history_from_dynamodb(city_name)

    # Fetch temperature and humidity data for the chart
    dates = [entry['date'] for entry in historical_weather]
    temperatures = [entry['temperature'] for entry in historical_weather]
    humidities = [entry['humidity'] for entry in historical_weather]

    # Fetch sensor data from S3
    s3_access_name = "cred-keys"
    secret = get_secrets(s3_access_name)

    bucket_name = "mycologeek"
    pacific_time = datetime.now(pacific_tz)
    sensor_file_name = f"sensors/{pacific_time.strftime('%Y-%m-%d')}-sensor-data.json"

    if secret:
        access_key = secret.get('access_key')
        secret_key = secret.get('secret_key')
        sensor_data = get_sensor_data(bucket_name, sensor_file_name, access_key, secret_key)
    else:
        sensor_data = None

    weather_condition = temperature['main'].lower()
    if "clear" in weather_condition:
        background_image = '../img/clear_sky.png'
    elif "rainy" in weather_condition:
        background_image = '../img/rainy_day.png'
    elif "thunderstorm" in weather_condition:
        background_image = '../img/rainy_day.png'
    elif "drizzle" in weather_condition:
        background_image = '../img/rainy_day.png'
    elif "snow" in weather_condition:
        background_image = '../img/snow_day.png'
    else:
        background_image = '../img/mushroom_bg.png'

    # Pass the data to the template
    return render_template('monitor.html', temperature=temperature, city=city_name, 
                           background_image=background_image, historical_weather=historical_weather, 
                           sensor_data=sensor_data, dates=dates, temperatures=temperatures, humidities=humidities)

@app.route('/technical.html')
def technical():
    return render_template('technical.html')

def fetch_post_metadata(slug):
    try:
        print(f"Fetching metadata for slug: {slug}")  # Log the slug being used
        response = table.get_item(Key={'PostID': slug})
        print(f"DynamoDB response: {response}")  # Log the full response from DynamoDB
        return response.get('Item')  # Return the metadata if it exists
    except Exception as e:
        print(f"Error fetching metadata from DynamoDB: {e}")
        return None

@app.route('/tags/<tag>')
def show_posts_by_tag(tag):
    try:
        # Scan DynamoDB for all posts that contain the specific tag
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('Tags').contains(tag)
        )
        posts = response.get('Items', [])
        
        # Sort posts by date (newest to oldest)
        posts = sorted(posts, key=lambda post: post['Date'], reverse=True)
        
        return render_template('tags.html', posts=posts, tag=tag)
    except Exception as e:
        print(f"Error fetching posts by tag: {e}")
        return "Error fetching posts by tag", 500


# Blog post route: fetch post from S3 and render it
@app.route('/blog/<slug>')
def blog_post(slug):
    # Fetch post metadata from DynamoDB
    metadata = fetch_post_metadata(slug)
    
    if not metadata:
        return "Post not found!", 404

    # Fetch the post content from S3 using the slug
    s3_post_key = f'blog/posts/{slug}/post.md'
    post_content_md = fetch_post_from_s3(S3_BUCKET, s3_post_key)

    if post_content_md is None:
        return "Post content not found!", 404

    # Convert the Markdown content to HTML
    post_content_html = markdown.markdown(post_content_md)

    # Render the post with metadata from DynamoDB
    return render_template(
        'post.html', 
        post_content=post_content_html, 
        title=metadata['Title'],  # Use title from DynamoDB metadata
        snippet=metadata.get('Snippet', 'No snippet available'),  # Optional fields
        featured_image_url=metadata.get('FeaturedImageURL', 'default-image.jpg')  # Optional image field
    )
@app.route('/articles/<name>')
def article(name):
    # Path to the Markdown file within the static folder
    filepath = os.path.join(app.static_folder, 'articles', f'{name}.md')

    # Check if the file exists
    if not os.path.exists(filepath):
        abort(404)  # If the file does not exist, return a 404 page

    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    return render_template('article.html', content=html_content, title=name)

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=8080)
