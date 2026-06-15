if st.button("Parse"):
    st.write("=== RAW TEXT ===")
    st.write(repr(text))

    lines = [l for l in text.split("\n") if l.strip()]

    st.write("=== LINES (VISIBLE) ===")
    st.write(lines)
