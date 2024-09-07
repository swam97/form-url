import random
import string
import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Database initialization
# Modify init_db function in app.py to update the schema

def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    # Modify the schema to include long_url and short_url fields
    cursor.execute('''
        DROP TABLE messages
    ''')
    cursor.execute('''
        
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            occasion TEXT NOT NULL,
            message TEXT NOT NULL,
            long_url TEXT,
            short_url TEXT
        )
    ''')
    conn.commit()
    conn.close()


def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    occasion = request.form['occasion']
    message = request.form['message']
    
    # Generate long URL (in this case, we'll just use a fake example for illustration)
    long_url = f"http://example.com/message/{random.randint(1000, 9999)}"
    
    # Generate a short URL (hash)
    short_url_hash = generate_short_url()
    short_url = f"http://localhost:5000/{short_url_hash}"

    # Store data in the database including long and short URLs
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (name, occasion, message, long_url, short_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, occasion, message, long_url, short_url))
    conn.commit()
    conn.close()

    return redirect(url_for('display_short_url', short_url=short_url))

@app.route('/display')
def display_short_url():
    short_url = request.args.get('short_url')
    return f"Your shortened URL is: <a href='{short_url}'>{short_url}</a>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)