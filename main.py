from flask import Flask, render_template
import random
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/random')
def random_number():
    return render_template("random.html", number=random.randint(0, 1000))

if __name__ == '__main__':
    app.run()