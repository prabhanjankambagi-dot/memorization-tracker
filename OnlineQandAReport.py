import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

st.set_page_config(page_title="Daily Memorization Tracker")

st.title("📘 Daily Byheart Tracker")

# -------------------------------
# Database connection
conn = sqlite3.connect("progress.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS progress(
    date TEXT PRIMARY KEY,
    questions INTEGER
)
""")

# -------------------------------
# DAILY ENTRY
st.header("Today's Entry")

today = str(date.today())

num_questions = st.number_input(
    "How many questions did you byheart today?",
    min_value=0,
    step=1
)

if st.button("Save Today’s Progress"):
    conn.execute(
        "INSERT OR REPLACE INTO progress VALUES (?, ?)",
        (today, num_questions)
    )
    conn.commit()
    st.success("✅ Progress Saved!")

# -------------------------------
# LOAD DATA
df = pd.read_sql("SELECT * FROM progress", conn)
df["date"] = pd.to_datetime(df["date"])

# -------------------------------
# WEEKLY REPORT
st.header("📊 Weekly Report")

if not df.empty:
    df["week"] = df["date"].dt.isocalendar().week

    current_week = df["week"].max()
    weekly_df = df[df["week"] == current_week]

    total_week = weekly_df["questions"].sum()

    st.metric("Questions This Week", total_week)

    st.line_chart(
        weekly_df.set_index("date")["questions"]
    )
else:
    st.info("No data yet.")

conn.close()