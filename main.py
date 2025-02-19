from flask import Flask, render_template, request
import random, json

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

DATA_FILE = "products.json"
USERS_FILE = "users.json"

def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file)

products = load_data(DATA_FILE)
users = load_data(USERS_FILE)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', products=products)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user-login')
        password = request.form.get('user-password')
        print(f"Username: {username}, Password: {password}")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('user-login')
        password = request.form.get('user-password')
        print(f"Username: {username}, Password: {password}")
    return render_template('register.html')

@app.route('/logout')
def logout():
    pass

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = 0
    for i in products:
        if i["id"] == id:
            product = i
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        products[products.index(product)] = {"id": id, "name": name, "description": description, "price": price, "image_url": image_url}
        save_products(products)
        return render_template('admin_panel.html', products=products)
    else:
        return render_template('edit.html', id=id, product=product)

@app.route('/admin', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        print(f"Name: {name}, Description: {description}, Price: {price}, URL: {image_url}")
        id = 1
        if len(products) > 0:
            id = products[-1]["id"] + 1
        if image_url:
            products.append({"id": id, "name": name, "description": description, "price": price, "image_url": image_url})
        else:
            products.append({"id": id, "name": name, "description": description, "price": price, "image_url": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQAHmXzY1cVOnJFUL3nRkxdpcA59vgdPmbdfb59zixgwFKwnkmYyQEg4JwDmVmi91xOUUtqCGF-ZrWxpiC--KtijPEdSWr0AcpcCQaM9uCC8_aJgpQAoNvshA&usqp=CAE"})
        save_products(products)

    return render_template('admin_panel.html', products=products)

@app.route('/delete/<int:id>')
def delete_product(id):
    if id > 0:
        for i in products:
            print(i)
            if i["id"] == id:
                index = products.index(i)
        products.pop(index)
        save_products(products)
    return render_template('admin_panel.html', products=products)

if __name__ == '__main__':
    app.run()