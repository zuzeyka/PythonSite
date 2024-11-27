from flask import Flask, render_template, redirect, url_for, request
import random, json
app = Flask(__name__)

DATA_FILE = "products.json"

def load_products():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_products(products):
    with open(DATA_FILE, "w") as file:
        json.dump(products, file)

products = load_products()

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

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    return render_template('edit.html', id=id)

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
            if i["id"] == id:
                index = products.index(i)
        products.pop(index)
        save_products(products)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run()