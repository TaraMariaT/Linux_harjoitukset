import os
from flask import Flask, jsonify, render_template, request
import mysql.connector
from dotenv import load_dotenv

# Load chat-specific .env
dotenv_path = '/home/ubuntu/mqtt-chat/.env'
load_dotenv(dotenv_path)

app = Flask(__name__, template_folder='templates')

@app.route('/chat/')
def chat():
    return render_template('chat/index.html')

@app.route('/api/messages')
def get_messages():
    limit = int(request.args.get('limit', 10))
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT nickname, message, created_at FROM messages ORDER BY created_at DESC LIMIT %s",
            (limit,)
        )
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(list(reversed(messages)))
    except Exception as e:
        import traceback
        print("ERROR in /api/messages:", e)
        traceback.print_exc()
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
