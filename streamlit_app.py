import streamlit as st
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from PIL import Image
import os

# Load environment variables
load_dotenv()  # expects DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

st.set_page_config(page_title="🐾 Cat Database", page_icon="🐱", layout="wide")

# --- Page background and general card CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #034d4d;  /* dark teal background */
    }
    .cat-card {
        background-color: #68ffc1;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(8,51,31,0.2);
        color: #08331f;
        margin-bottom: 20px;
        transition: 0.2s;
    }
    .cat-card:hover {
        filter: brightness(1.05);
    }
    .progress-bar-container {
        position: relative;
        background-color: #08331f;
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 6px;
    }
    .progress-bar-fill {
        background-color: #21f893;
        height: 20px;
    }
    .progress-bar-label {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        color: white;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🐾 Cat Info Database")
st.subheader("Meet the Cats 😺")

# Emoji placeholders if no image exists
cat_emojis = {
    "Vili": "🐱",
    "Shura": "😸",
    "Gin": "😺",
    "Ren": "😻"
}

# Function to find image for a cat
def find_image(cat_name):
    for ext in ["jpg", "JPG", "png", "PNG"]:
        path = f"Images/{cat_name}.{ext}"  # folder Images
        if os.path.exists(path):
            return path
    return None

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Load cat data
try:
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM cats;", conn)
    st.success("✅ Successfully loaded cat data from MySQL!")

    # Find oldest cat for scaling progress bars
    max_age = df['age'].max()

    # Display cats in a 2-column grid
    cols = st.columns(2)
    for i, (_, cat) in enumerate(df.iterrows()):
        with cols[i % 2]:
            image_path = find_image(cat['name'])
            if image_path:
                img = Image.open(image_path)
                img = img.resize((120, 120))
                st.image(img)
            else:
                st.markdown(f"<div style='font-size:72px;text-align:center;'>{cat_emojis.get(cat['name'], '🐱')}</div>", unsafe_allow_html=True)

            st.markdown(f"""
                <div class='cat-card'>
                    <h3>{cat['name']} — {cat['age']} years old</h3>
                    <p><b>Personality:</b> {cat['personality']} 😸</p>
                    <p><b>Favorite food:</b> {cat['favorite_food']} 🍗</p>
                    <p><b>Age progress:</b></p>
                    <div class='progress-bar-container'>
                        <div class='progress-bar-fill' style='width:{cat["age"]/max_age*100}%;'></div>
                        <div class='progress-bar-label'>{cat['age']} yrs</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("All Cats Ages")
    st.bar_chart(df.set_index('name')['age'])

except Exception as e:
    st.error(f"❌ Database error: {e}")

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
