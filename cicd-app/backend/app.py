from flask import Flask, jsonify
import os
import mysql.connector
import platform
import socket
from datetime import datetime

app = Flask(__name__)

# --- Config ---
DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')

START_TIME = datetime.utcnow()

# --- Health check ---
@app.get('/api/health')
def health():
    return jsonify(message={"status": "ok"})

# --- DB time ---
@app.get('/api/time')
def time():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(message={"time": str(row[0])})

# --- DB greeting ---
@app.get('/api')
def index():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MySQL via CI/CD!'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(message=row[0])

# --- NEW FEATURE: runtime info ---
@app.get('/api/info')
def info():
    uptime = datetime.utcnow() - START_TIME
    return jsonify({
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
        "uptime_seconds": int(uptime.total_seconds()),
        "db_host": DB_HOST
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
