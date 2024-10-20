# Rebuilding the Mycologeek Blog From Monolithic Page to a Modern, Scalable Platform
*by Ryan Dagley*

When I first launched Mycologeek, my website was a passion project that combined my love of fungi with my technical knowledge. It had a single, monolithic page for the blog, which included every post, image, and snippet hard-coded in HTML. It worked initially, but over time, this setup became a nightmare to maintain. Not only did everything load at once, causing slow performance, but adding new content meant manually updating the page and redeploying the whole site.

The blog was quickly turning into an unmanageable beast, and it was clear that I needed a better solution. Enter AWS.

In this blog post, I’ll walk you through the journey of rebuilding Mycologeek's blog using AWS services like S3, DynamoDB, Lambda, API Gateway, and CloudFront. This new setup allowed me to make the blog SEO-friendly, scalable, and much easier to maintain.

## The Monolithic Problem
Initially, all the blog content was embedded directly into a single HTML file. This meant that every time a user visited the blog, they had to download the entire page, including all images and posts, regardless of how much of the content they intended to read. This not only slowed down the page load times but also made it harder for search engines to crawl and index individual posts.

## Key Problems:

- **Performance:** The page became slower and slower as more posts were added. Every post, image, and snippet loaded upfront, overwhelming both the browser and the server.
- **Maintenance:** Adding a new post meant manually updating the HTML and redeploying the entire website. It was clunky and inefficient.
- **SEO Challenges:** With everything packed into a single page, individual posts didn’t have unique URLs, making it harder for search engines to index and rank the blog properly.

## The Design Process
After living with this monolithic setup for a while, I realized I needed a change. I outlined a new design that would break the blog into individual posts, each with its own URL, and would use a scalable backend powered by AWS.

This was the beginning of the Mycologeek blog rebuild, a design that leveraged the following AWS services:

## AWS Services:
S3 (Simple Storage Service): For storing blog content (in Markdown format) and images.
DynamoDB: For storing metadata about each post, such as the title, date, tags, and URLs.
Lambda: For processing requests and dynamically fetching content from S3 and DynamoDB.
API Gateway: To serve as the interface between the frontend and backend.
CloudFront: To deliver the content globally and cache responses to improve performance.
This modular approach would allow the blog to be more scalable, easier to maintain, and SEO-friendly.

## Building the New Blog
### Step 1: Breaking Up the Monolith
The first step was to divide the single HTML blog into individual blog posts. Each post would now have its own Markdown file stored in S3. This separation allowed me to easily add new content without touching the entire site. The folder structure in S3 was designed to organize posts by year and slug, like this:

```
/mycologeek-blog
    /posts
        /2024
            /2024-10-07-fungi-adventure
                - post.md
                - featured-image.jpg
                - fungi-image-1.jpg
            /2024-10-15-mushroom-magic
                - post.md
                - featured-image.jpg
```

### Step 2: Metadata in DynamoDB
Each blog post needed metadata—such as the title, date, tags, and featured image—so I decided to store this information in DynamoDB. This allows me to quickly query the database to generate a blog landing page and to filter posts by tag.

The DynamoDB schema looked something like this:

```
Table: BlogPosts
Primary Key: PostID (e.g., 2024-10-07-fungi-adventure)
Attributes:
  - Title
  - Date
  - Excerpt
  - FeaturedImageURL
  - Tags
  - PostURL
```


This setup provided a simple way to fetch metadata for the blog landing page and individual post pages.

### Step 3: Using Lambda and API Gateway
To dynamically fetch content from S3 and DynamoDB, I created several Lambda functions that were triggered by API Gateway:

- **Fetch Blog Metadata:** This function queries DynamoDB for all blog metadata, returning a list of posts with titles, dates, tags, and featured images.
- **Fetch Individual Post Content:** This function fetches a specific post’s content from S3, converts the Markdown to HTML, and returns the full post with metadata.

### Step 4: Building the Frontend
On the frontend, I created a new blog landing page that dynamically fetched blog metadata from the API Gateway. Each post is displayed with a title, date, featured image, and a short excerpt. Users can click on a post to navigate to its full page.

I also implemented tag filtering so users could browse posts by categories like “Fungi” or “Experiments.” Clicking on a tag would trigger an API request to fetch posts associated with that tag.

## Step 5: SEO and Performance Optimization
One of my main goals was to improve the SEO of Mycologeek’s blog. To achieve this, I ensured that:

- **Unique URLs:** Each post had its own SEO-friendly URL (e.g., /blog/2024-10-07-fungi-adventure).
- **Meta Tags:** I added meta tags for each post, including titles, descriptions, OpenGraph, and Twitter Card data.
- **CloudFront Caching:** To improve performance, I used CloudFront to cache both static assets (like images) and dynamic content (API responses), reducing load times significantly.

## Challenges Along the Way
Rebuilding the blog wasn’t without its challenges. One of the toughest parts was managing the asynchronous nature of fetching data from multiple AWS services. I had to ensure that the frontend was able to handle dynamic data fetching smoothly, without causing delays for users.

Additionally, ensuring that the blog was SEO-friendly required careful attention to structured data, meta tags, and OpenGraph properties. Each post needed to have well-defined meta tags to improve discoverability.

## Final Thoughts
By rebuilding Mycologeek’s blog with AWS, I was able to transform the site from a clunky, monolithic page into a modern, scalable platform that’s easy to manage and optimized for search engines. Blog posts can now be added by simply uploading a Markdown file and updating DynamoDB with the necessary metadata.

With the new setup, I’ve laid the foundation for future growth. There’s room to add features like a search function, comments, and even an admin interface. I can now focus more on creating content without worrying about the technical overhead of maintaining a monolithic HTML blog.

If you're thinking about building your own blog platform or revamping an old one, leveraging cloud services like AWS can give you the flexibility and scalability you need without the headaches of maintaining a traditional server-based setup.

Stay tuned for more technical insights, mushroom adventures, and tips on managing your own digital projects!

## Conclusion
Rebuilding the Mycologeek blog using AWS was a rewarding journey that not only improved the performance and scalability of the site but also made it a joy to maintain. I’m excited about the future of the blog, and I hope this post gives you some inspiration for your own projects.

Have questions about the process? Feel free to reach out!