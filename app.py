import random
import string
import sqlite3
from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

# Database initialization
# Modify init_db function in app.py to update the schema

def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    # Modify the schema to include long_url and short_url fields
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


# Function to generate a random short URL if no custom alias is provided
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
    custom_alias = request.form['custom_alias']

    # Generate long URL (for this example, using a dummy long URL)
    long_url = f"http://example.com/message/{random.randint(1000, 9999)}"
    
    # Use the custom alias if provided; otherwise, generate a short URL
    if custom_alias:
        short_url = f"http://localhost:5000/{custom_alias}"
    else:
        short_url_hash = generate_short_url()
        short_url = f"http://localhost:5000/{short_url_hash}"

    # Store data in the database including long and short URLs
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    # Check if the custom alias already exists in the database
    if custom_alias:
        cursor.execute("SELECT 1 FROM messages WHERE short_url = ?", (short_url,))
        if cursor.fetchone():
            return jsonify({'error': 'Custom alias already exists. Please choose a different one.'}), 400
            # return "Error: Custom alias already exists. Please choose a different one."

    cursor.execute('''
        INSERT INTO messages (name, occasion, message, long_url, short_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, occasion, message, long_url, short_url))

    conn.commit()
    conn.close()
    return jsonify({'success': 'Message submitted successfully!', 'short_url': short_url}), 200
    # return redirect(url_for('display_short_url', short_url=short_url))
    # return redirect(url_for('display_short_url', alias=custom_alias or short_url.split('/')[-1]))


@app.route('/display')
def display_short_url():
    short_url = request.args.get('short_url')
    return f"Your customized URL is: <a href='{short_url}'>{short_url}</a>"
    # alias = request.args.get('alias')
    # short_url = f"http://localhost:5000/{alias}"
    # return f"Your customized URL is: <a href='{short_url}'>{alias}</a>"

if __name__ == '__main__':
    app.run(debug=True)