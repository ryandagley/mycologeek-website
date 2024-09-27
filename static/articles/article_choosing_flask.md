# Why I Chose Flask for My Website

## Date: Sometime late 2020, Last updated September 2024

<img src="../static/img/articles/python.png" alt="description" style="float: left; margin-right: 20px; width: 30%; max-width: 100%;" />
A few years ago, I found myself wanting to learn more about Python. I was working in data analytics at the time, so Python was somewhat common in my job, but its use fell far short of SQL. While I already had a basic understanding of HTML and CSS, and some very basic JavaScript, none of those skills had much practical usage in my day-to-day work. Python, on the other hand, seemed like something worth diving deeper into. Fast forward to today, and I’m still very much a student of Python, though my job role has since changed.

Initially, my website was a collection of static HTML files that I hosted in an S3 bucket on AWS. It worked fine for what it was, but it wasn’t particularly impressive, and it didn’t provide the opportunity to work with Python, which was something I wanted. So, I set out to rebuild my site using Flask, a lightweight Python web framework. At first, I was still manually copying all the files over to S3, but eventually, I found a better way.

<div style="clear: both;"></div>

---


## Benefits of Python and Flask for Web Development

There are several reasons I chose Flask and Python for web development:

1. **Simplicity**: Flask is a micro-framework, which means it's relatively small and simple to use. This makes it a great choice for smaller projects where you don’t need the complexity of a full-stack framework like Django.  I didn't really understand that, but I remember thinking Django seemed more difficult.
   
2. **Flexibility**: Flask doesn't come with a lot of built-in components, giving you the flexibility to choose the tools and libraries that work best for your project. This allowed me to create a setup that aligned with what I wanted to learn and none of the extras!

3. **Python**: Python itself is a powerful and versatile language. It’s widely used in data analytics, machine learning, automation, and web development. Using Flask for web development gave me the chance to continue improving my Python skills while working on a project I cared about.

4. **Learning Opportunity**: Because Flask is minimalistic, it forces you to learn about the building blocks of web development, like routing, templating, and request handling. This hands-on learning helped me better understand how web applications work behind the scenes.

<div style="clear: both;"></div>

---

<img src="../static/img/articles/flask2.png" alt="description" style="float: right; margin-left: 10px; width: 30%; max-width: 100%;" />



## The Reality of Using Flask

While I enjoy working with Python and Flask, I understand that Flask isn't the most sought-after framework in the web development world. A lot of people are leaning towards JavaScript frameworks like React, especially since JavaScript is so prevalent on the front end. But for me, this is a side project, and I have to balance my time, energy, and (unfortunately) limited mental capacity. I need to focus on building skills that make sense for me overall, rather than spreading myself thin across too many technologies.

That said, it’s hard for me to say that I’m truly learning Python deeply by using Flask. Yes, it teaches me some Python syntax and best practices, but I'm mostly learning a specific use-case for Python in web development. And you know what? That’s okay. It’s part of the learning process. 

In some ways, choosing Flask also forced me to think about how I wanted to deploy my website. This led me to explore AWS Elastic Beanstalk, which has been a valuable, and sometimes very frustrating, learning experience in itself (I'll write about Elastic Beanstalk in another article). 

<div style="clear: both;"></div>
---

## The Next Step: Structuring and Compartmentalizing My Flask App

Now that I've built a few things in Flask, I’ve started wondering about how to better compartmentalize my code. I’ve grown comfortable with Flask’s program structure, but it feels like I could offload some components and content externally to make the whole thing easier to work with. 

Right now, everything is bundled together, and it works, but as the project grows, it makes sense to think about separating concerns. For example, I could host static content like images, CSS, and JavaScript in S3 and keep the dynamic parts in Flask. Doing so could improve performance and make updates easier to manage over my current method of hardcoding content.

I’m still figuring this part out, but it’s a good challenge. For now, I’m focusing on keeping the codebase clean and organized, so it remains maintainable as the site evolves.

---

That's a brief overview of why I chose Flask, how I got it set up, and where I'm headed next. Flask might not be the most popular framework out there, but it works for me and continues to help me grow as a Python developer. And at the end of the day, that’s what matters.
