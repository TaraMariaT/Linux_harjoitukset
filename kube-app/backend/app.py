from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# --- Database connection helper ---

def db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# --- Basic health endpoint ---

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})


# --- Initialize database with cats + users ---

@app.route("/api/init-db")
def init_db():
    try:
        conn = db()
        cur = conn.cursor()

        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)

        # Add UNIQUE constraint to prevent duplicates
        try:
            cur.execute("ALTER TABLE users ADD UNIQUE (email)")
        except:
            pass  # already unique

        # Insert demo users only if table empty
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
            cur.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")


        # Create cats table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                favorite_food VARCHAR(100),
                personality VARCHAR(255),
                weight_kg FLOAT,
                votes INT DEFAULT 0
            )
        """)

        # Add cats only if table empty
        cur.execute("SELECT COUNT(*) FROM cats")
        if cur.fetchone()[0] == 0:
            cur.execute("""
                INSERT INTO cats (name, age, favorite_food, personality, weight_kg)
                VALUES
                ('Vili', 14, 'Plastic', 'Loud', 4.6),
                ('Shura', 9, 'Raw meatballs', 'Angry looking but very cuddly', 2.8),
                ('Gin', 8, 'Not too picky', 'Has no thoughs', 3.2),
                ('Ren', 6, 'Anything', 'Always friendly, food motivated', 5.9)
            """)

        conn.commit()
        return jsonify({"message": "database initialized with cats + users"})

    except Exception as e:
        return jsonify({"error": str(e)})


# --- Get all cats ---

@app.route("/api/cats")
def get_cats():
    try:
        conn = db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM cats ORDER BY votes DESC")
        cats = cur.fetchall()
        return jsonify(cats)
    except Exception as e:
        return jsonify({"error": str(e)})


# --- Vote for a cat ---

@app.route("/api/vote/<int:cat_id>", methods=["POST"])
def vote(cat_id):
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("UPDATE cats SET votes = votes + 1 WHERE id = %s", (cat_id,))
        conn.commit()
        return jsonify({"message": "vote added", "cat_id": cat_id})
    except Exception as e:
        return jsonify({"error": str(e)})


# --- Get all users ---

@app.route("/api/users")
def users():
    try:
        conn = db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users")
        users_list = cur.fetchall()
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)})


# --- Start Flask ---

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
