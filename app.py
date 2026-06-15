import streamlit as st

if st.button("Parse"):
    st.write("=== RAW INPUT ===")
    st.write(text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    st.write("=== LINES ===")
    st.write(lines)
