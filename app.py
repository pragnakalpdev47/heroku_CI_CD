from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Initialize the database if it doesn't exist
def init_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert data into the database
def insert_user(name, email, password):
    hashed_password = generate_password_hash(password)  # Encrypt the password
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, email, password) 
        VALUES (?, ?, ?)
    ''', (name, email, hashed_password))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        # Insert data into the database
        insert_user(name, email, password)
        
        return redirect(url_for("success"))
    return render_template("form.html")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    init_db()  # Initialize the database when the app starts
    app.run(host="0.0.0.0", port=5000)
