from flask import Flask, render_template
import json, random, requests

# define the app variable as Flask
#app = Flask(__name__, template_folder="templates")
app = Flask(__name__)


# Routes to the templates
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

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
    return render_template('monitor.html')


@app.route('/pipe/', methods=["GET", "POST"])
def pipe():
    payload = {}
    headers = {}
    url = "https://s3-us-west-2.amazonaws.com/mycologeek.com/sensor_data.json"
    r = requests.get(url, headers=headers, data ={})
    r = r.json()
    return {"res":r}

@app.route('/technical.html')
def technical():
    return render_template('technical.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)