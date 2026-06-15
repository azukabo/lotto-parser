import streamlit as st

st.title("Lotto Parser")

text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    # debug แบบปลอดภัยสุด
    lines = text.split("\n")
    st.write("INPUT LINES:")
    st.write(lines)
