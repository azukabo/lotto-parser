import streamlit as st
import re

st.title("Lotto Parser (Safe Mode)")

def parse_order(text):
    results = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^\s*(\d{1,3})", line)
        if not m:
            continue

        n = m.group(1)

        price_match = re.findall(r"\d+(?:\*\d+)*", line)
        if not price_match:
            continue

        last = price_match[-1]
        price = [int(x) for x in last.split("*")] if "*" in last else [int(last)]

        results.append(f"{n} {price[0]} 0 0")

    return results


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    st.write(parse_order(text))
