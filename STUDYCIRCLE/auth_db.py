from sqlalchemy import create_engine
import streamlit as st

try:
    MYSQL_USER = st.secrets["mysql"]["user"]
    MYSQL_PASSWORD = st.secrets["mysql"]["password"]
    MYSQL_HOST = st.secrets["mysql"]["host"]
    MYSQL_PORT = st.secrets["mysql"]["port"]
    MYSQL_DB = "circle"

    engine = create_engine(
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    conn = engine.connect()

except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
