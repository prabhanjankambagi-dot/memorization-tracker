import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Family App")

st.title("👨‍👩‍👧 Family Members")

# -----------------------------
# Database
conn = sqlite3.connect("family.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS family_member(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

# -----------------------------
# Add member
st.header("Add Family Member")

name = st.text_input("Enter name")

if st.button("Add Member"):
    if name:
        conn.execute(
            "INSERT INTO family_member (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        st.success("Member added!")
    else:
        st.warning("Enter a name")

# -----------------------------
# Show members
st.header("Family Members")

df = pd.read_sql("SELECT name FROM family_member", conn)

st.dataframe(df)

conn.close()
