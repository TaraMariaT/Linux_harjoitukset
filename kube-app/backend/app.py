from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/init-db")
def init_db():
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        cur.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
        cur.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
        conn.commit()
        return jsonify({"message": "initialized"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/users")
def users():
    try:
        conn = db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
