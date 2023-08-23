from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__, static_folder='static')
current_directory = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(current_directory, 'sulit.db')
app.secret_key = 'SKSuL!t'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not all([username, password]):
            error_message = "Please enter valid information(s)!"
            return render_template('login.html', error_message=error_message)
        
        if username and password:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username = ? LIMIT 1", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and user[2] == password:
                flash("Successfully logged in!", "success")
                session['id'] = user[0]
                
                return redirect(url_for('index'))

        error_message = "Wrong username or password!"
        return render_template('login.html', error_message=error_message)
    
    if session.get('just_logged_out'):
        flash("Successfully logged out!", "success")
        session.pop('just_logged_out', None)

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    if 'id' in session:
        session.pop('id', None)
        flash("Successfully logged out!", "success")
        session['just_logged_out'] = True  


    return redirect(url_for('login', logout_msg='yes'))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        suffix = request.form['suffix']

        if not all([username, password, firstname, lastname]):
            msg = "Please enter valid information(s)!"
            return render_template('register.html', msg=msg)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = "The Username you entered has been taken!"
            conn.close()
            return render_template('register.html', msg=msg)

        cursor.execute("INSERT INTO user (username, password, first_name, middle_name, last_name, suffix) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, password, firstname, middlename, lastname, suffix))
        conn.commit()
        conn.close()

        flash("Successfully registered! You can now login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Home page route
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Search route
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search', '')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_name LIKE ?", ('%' + search_query + '%',))
    products = cursor.fetchall()
    conn.close()

    return render_template('search.html', products=products, search_query=search_query)

# Product page route
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_page(product_id):
    if request.method == 'POST':
        qty = request.form.get('qty', 1)

        try:
            qty = int(qty)
            if qty <= 0:
                flash("Invalid quantity. Please enter a valid quantity.", "error")
            else:
                conn = sqlite3.connect(DATABASE)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
                product = cursor.fetchone()

                if not product:
                    flash("Product not found.", "error")
                else:
                    if 'cart' not in session:
                        session['cart'] = []

                    cart_items = session['cart']
                    for item in cart_items:
                        if item['prodid'] == product_id:
                            item['qty'] += qty
                            break
                    else:
                        cart_items.append({'prodid': product_id, 'qty': qty, 'price': product['price'], 'name': product['product_name'], 'img': product['img_dir']})

                    flash(f"Added {qty} {product['product_name']} to the cart.", "success")

                conn.close()

        except ValueError:
            flash("Invalid quantity. Please enter a valid quantity.", "error")

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if not product:
        flash("Product not found.", "error")
        return redirect(url_for('index')) 

    return render_template('product_page.html', product=product, product_id=product_id)

# Checkout route
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        if 'cart' in session:
            cart_items = session['cart']
            total = 0
            for item in cart_items:
                total += item['price'] * item['qty']

            payment_method = request.form.get('payment_method')
            shipping_address = request.form.get('shipping_address')

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            for item in cart_items:
                qty = item['qty']
                product_id = item['prodid']
                cursor.execute("UPDATE products SET quantity = CASE WHEN quantity >= ? THEN quantity - ? ELSE 0 END WHERE id = ?",
                               (qty, qty, product_id))
            conn.commit()
            conn.close()

            session.pop('cart', None)

            flash("Payment successful!", "success") 
            return redirect(url_for('index'))
        
    total = 0
    if 'cart' in session:
        cart_items = session['cart']
        for item in cart_items:
            total += item['price'] * item['qty']

    print("DEBUG: Total in checkout route:", total)

    if 'cart' in session:
        cart_items = session['cart']
        return render_template('checkout.html', cart=cart_items, total=total)
    else:
        return render_template('checkout.html', cart=None, total=total)
    
# Route remove from cart    
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session:
        cart_items = session['cart']
        session['cart'] = [item for item in cart_items if item['prodid'] != product_id]
        flash("Item removed from the cart.", "success")
    else:
        flash("Cart is empty.", "error")
    
    return redirect(url_for('checkout'))

# Route to empty cart
@app.route('/empty_cart')
def empty_cart():
    if 'cart' in session:
        session.pop('cart', None)
        flash("Cart is now empty.", "success")
    else:
        flash("Cart is already empty.", "error")
    
    return redirect(url_for('checkout', empty=1))

if __name__ == '__main__':
    app.run(debug=True)