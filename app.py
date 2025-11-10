from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    # Connect to MySQL using environment variables
    conn = mysql.connector.connect(
        host="localhost",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()
    cursor.execute("SELECT NOW()")
    current_time = cursor.fetchone()
    cursor.close()
    conn.close()

    # Return HTML as an f-string so variables are evaluated
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>LEMP site</title>
<style>
:root {{
    --green-main: rgba(33, 248, 147, 0.9);
    --green-darker: rgba(22, 180, 110, 0.95);
    --green-lighter: rgba(104, 255, 193, 0.95);
    --green-pale: rgba(255, 255, 255, 0.9);
    --text: #08331f;
    --muted-shadow: rgba(8,51,31,0.08);
}}
html,body{{height:100%;margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;background: var(--green-main); color:var(--text);}}
.wrap{{min-height:100%;display:flex;align-items:center;justify-content:center;padding:40px}}
.card{{background: var(--green-lighter); border-radius:12px; padding:22px; max-width:820px; display:grid; grid-template-columns:120px 1fr; gap:18px; box-shadow:0 8px 30px var(--muted-shadow); outline: 1px solid rgba(0,0,0,0.04);}}
.avatar{{width:110px; height:110px; border-radius:10px; background: var(--green-darker); display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:36px;}}
.details{{background: linear-gradient(var(--green-pale), transparent); padding:10px 14px; border-radius:8px;}}
h1{{margin:0 0 6px 0;font-size:22px}}
p{{margin:0 0 10px 0;line-height:1.4}}
pre{{font-family:monospace;}}
@media (max-width:560px){{.card{{grid-template-columns:1fr;align-items:start}} .avatar{{margin:0 auto}} .details{{background:transparent;padding:0}}}}
</style>
</head>
<body>
<div class="wrap">
    <section class="card">
        <div class="avatar">💡</div>
        <div class="details">
            <h1>Hello — Welcome to my Linux assignment site!</h1>
            <p>This small site demonstrates a Flask app connecting to MySQL.</p>
            <pre>
 _._     _,-'""`-._
(,-.`._,'(       |\\`-/|
    `-.-' \\ )-`( , o o)
          `-    \\`_`"'- 
            </pre>
            <p>MySQL says: {result[0]}</p>
            <p>Server time: {current_time[0]}</p>
        </div>
    </section>
</div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
