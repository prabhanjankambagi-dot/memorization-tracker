import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# -----------------------
# Database Connection
# -----------------------
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memorization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date TEXT,
    questions INTEGER
)
""")
conn.commit()

# -----------------------
# UI
# -----------------------
st.title("📘 Daily Memorization Tracker")

today = date.today()

st.subheader("Enter Today's Progress")

num_questions = st.number_input(
    "How many questions did you memorize today?",
    min_value=0,
    step=1
)

if st.button("Save Today’s Entry"):
    cursor.execute(
        "INSERT INTO memorization (entry_date, questions) VALUES (?, ?)",
        (str(today), num_questions)
    )
    conn.commit()
    st.success("Saved successfully!")

# -----------------------
# Show All Data
# -----------------------
st.subheader("📅 All Entries")

df = pd.read_sql("SELECT * FROM memorization", conn)

if not df.empty:
    st.dataframe(df)

# -----------------------
# Weekly Report
# -----------------------
st.subheader("📊 Weekly Report")

if not df.empty:
    df["entry_date"] = pd.to_datetime(df["entry_date"])
    df["week"] = df["entry_date"].dt.isocalendar().week

    weekly = df.groupby("week")["questions"].sum().reset_index()

    st.bar_chart(weekly.set_index("week"))
