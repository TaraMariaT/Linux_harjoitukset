import streamlit as st 
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from PIL import Image
import os

# Load environment variables
load_dotenv()  # expects DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

st.set_page_config(page_title="🐾 Cat & Weather Database", page_icon="🐱", layout="wide")

# ===== CSS STYLING =====
st.markdown(
    """
    <style>
    .stApp {
        background-color: #034d4d;
    }
    .cat-card, .weather-card, .iss-card {
        background-color: #68ffc1;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(8,51,31,0.2);
        color: #08331f;
        margin-bottom: 20px;
        transition: 0.2s;
    }
    .cat-card:hover, .weather-card:hover, .iss-card:hover {
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

# ===== SIDEBAR =====
page = st.sidebar.selectbox("Select database view", ["Cats", "Weather", "ISS"])

# ===== MYSQL CONNECTION =====
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ===== FINNISH TIME CONVERSION =====
def to_finnish_time(ts):
    if isinstance(ts, str):
        ts = pd.to_datetime(ts)

    # Make naive timestamps UTC
    if ts.tzinfo is None or ts.tzinfo.utcoffset(ts) is None:
        ts = ts.tz_localize("UTC")

    # Convert to Helsinki
    ts = ts.tz_convert("Europe/Helsinki")

    # Format without seconds
    return ts.strftime("%d.%m.%Y %H:%M")

# ===== CATS PAGE =====
if page == "Cats":
    st.title("🐾 Cat Info Database")
    st.subheader("Meet the Cats 😺")

    cat_emojis = {"Vili": "🐱", "Shura": "😸", "Gin": "😺", "Ren": "😻"}

    def find_image(cat_name):
        for ext in ["jpg", "JPG", "png", "PNG"]:
            path = f"Images/{cat_name}.{ext}"
            if os.path.exists(path):
                return path
        return None

    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM cats;", conn)
        st.success("✅ Successfully loaded cat data from MySQL!")

        max_age = df['age'].max()
        cols = st.columns(2)

        for i, (_, cat) in enumerate(df.iterrows()):
            with cols[i % 2]:
                image_path = find_image(cat['name'])
                if image_path:
                    img = Image.open(image_path).resize((120, 120))
                    st.image(img)
                else:
                    st.markdown(
                        f"<div style='font-size:72px;text-align:center;'>{cat_emojis.get(cat['name'], '🐱')}</div>",
                        unsafe_allow_html=True
                    )

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

# ===== WEATHER PAGE =====
elif page == "Weather":
    st.title("🌤️ Weather Data (Helsinki)")

    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50;", conn)
        st.success("✅ Successfully loaded weather data!")

        # Convert timestamps
        df['timestamp'] = df['timestamp'].apply(to_finnish_time)

        # Chart at top
        st.subheader("Temperature over time")
        st.line_chart(df.set_index('timestamp')['temperature'])

        # Cards below
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class='weather-card'>
                    <p><b>City:</b> {row['city']}</p>
                    <p><b>Temperature:</b> {row['temperature']} °C</p>
                    <p><b>Description:</b> {row['description']}</p>
                    <p><b>Timestamp:</b> {row['timestamp']}</p>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Database error: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# ===== ISS PAGE =====
elif page == "ISS":
    st.title("🛰️ ISS Current Location")

    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM iss_data ORDER BY timestamp DESC LIMIT 50;", conn)
        st.success("✅ Successfully loaded ISS data!")

        # Convert timestamps
        df['timestamp'] = df['timestamp'].apply(to_finnish_time)

        # Chart at top (map)
        st.subheader("ISS Path over time")
        map_df = df.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
        st.map(map_df)

        # Cards below
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class='iss-card'>
                    <p><b>Latitude:</b> {row['latitude']}</p>
                    <p><b>Longitude:</b> {row['longitude']}</p>
                    <p><b>Timestamp:</b> {row['timestamp']}</p>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Database error: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
