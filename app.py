from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import re  # Import regex for blacklist filtering
import urllib.parse  # Import for URL decoding

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Use SECRET_KEY from .env (fallback to a default if not set)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Connect to MySQL Database using .env variables
try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'catbooks_db'),
        charset='utf8mb4',
        collation='utf8mb4_unicode_ci'
    )
    cursor = conn.cursor()
    print("[✔] Connected to the database successfully!")
except mysql.connector.Error as err:
    print(f"[❌] Database connection error: {err}")


@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        return render_template('contact.html', name=name, message=message, submitted=True)
    return render_template('contact.html', submitted=False)

@app.route('/shop')
def shop():
    cursor.execute("SELECT id, title, author, price, image FROM books")
    books = cursor.fetchall()
    return render_template('shop.html', books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    cursor.execute("SELECT id, title, author, price, image FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if book:
        return render_template('book_details.html', book=book)
    else:
        return "Book not found", 404

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    items = []
    total = 0
    for book_id in cart:
        cursor.execute("SELECT id, title, price FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        if book:
            items.append(book)
            total += book[2]
    return render_template('cart.html', items=items, total=total)

@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(book_id)
    session.modified = True
    return redirect(url_for('shop'))

@app.route('/remove_from_cart/<int:book_id>', methods=['POST'])
def remove_from_cart(book_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item != book_id]
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/returns', methods=['GET', 'POST'])
def returns():
    if request.method == 'POST':
        return render_template('returns.html', submitted=True)
    return render_template('returns.html')

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        review_text = request.form.get('review')
        file = request.files.get('file')
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cursor.execute("INSERT INTO reviews (review_text, image) VALUES (%s, %s)", (review_text, filename))
        conn.commit()
    cursor.execute("SELECT id, review_text, image FROM reviews")
    reviews = cursor.fetchall()
    return render_template('reviews.html', reviews=reviews)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
    conn.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/search')
def search():
    query = request.args.get('query', '')

    # Apply blacklist BEFORE decoding to bypass encoded filters
    blacklisted_query = re.sub(r"\b(UNION|SELECT|union|select)\b", "blocked", query)

    # Decode URL-encoded payloads AFTER blacklist
    filtered_query = urllib.parse.unquote(blacklisted_query)

    # Filter out single quotes
    filtered_query = filtered_query.replace("'", "")

    try:
        # Vulnerable SQL query
        vulnerable_query = f'SELECT id, title, author, price FROM books WHERE title = "{filtered_query}" -- '
        print(f"Executing SQL Query: {vulnerable_query}")  # Debugging line
        cursor.execute(vulnerable_query)
        results = cursor.fetchall()
    except Exception as e:
        results = []
        print(f"SQL Error: {e}")

    return render_template('search.html', results=results, query=query)



@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    return redirect(url_for('home'))

# Regular User Login (Vulnerable)
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        try:
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            users = cursor.fetchall()

            # Extract additional data via SQL injection, if present
            extracted_data = None
            if cursor.description and cursor.rowcount > 0:
                extracted_data = users[0][1]  # Assuming username or injected data appears here

            # Check if extracted data exists as a real user
            cursor.execute("SELECT username FROM users")
            real_users = [row[0] for row in cursor.fetchall()]

            # Allow login if it's a real user (even via injection)
            if extracted_data in real_users:
                session['user'] = extracted_data
                message = f"✅ Welcome, {session['user']}!"
            elif extracted_data:
                message = f"⚠️ Extracted Data: {extracted_data}"
            else:
                message = "❌ Login Failed."

        except Exception as e:
            message = f"⚠️ Error: {str(e)}"

    return render_template('login.html', message=message)



# Secure Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            session['user'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            message = "❌ Admin Login Failed."
    return render_template('admin_login.html', message=message)

# Admin Dashboard Route
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        price = request.form.get('price')
        image = request.files.get('image')

        image_filename = None
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        cursor.execute(
            "INSERT INTO books (title, author, price, image) VALUES (%s, %s, %s, %s)",
            (title, author, price, image_filename)
        )
        conn.commit()

        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT id, title, author, price, image FROM books")
    books = cursor.fetchall()
    cursor.execute("SELECT id, review_text, image FROM reviews")
    reviews = cursor.fetchall()
    return render_template('admin_dashboard.html', books=books, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
