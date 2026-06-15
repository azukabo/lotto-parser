import streamlit as st

st.title("Lotto Parser")

text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    st.write(text)
