import streamlit as st
import re

st.title("Lotto Parser")

def parse_order(text):
    results = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        tokens = line.split()

        numbers = []
        price = []

        for t in tokens:
            if t.isdigit() and len(t) <= 3:
                numbers.append(t)
            elif "*" in t:
                price = [int(x) for x in t.split("*")]
            elif t.isdigit() and len(t) > 3:
                # เผื่อ case 100200
                price = [int(t)]

        if not numbers or not price:
            continue

        for n in numbers:
            if len(price) == 1:
                results.append(f"{n} {price[0]} 0 0")
            elif len(price) == 2:
                results.append(f"{n} {price[0]} {price[1]} 0")
            elif len(price) == 3:
                results.append(f"{n} {price[0]} {price[1]} {price[2]}")

    return results


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    result = parse_order(text)

    st.subheader("ผลลัพธ์")

    if not result:
        st.warning("ไม่มีข้อมูลที่ parse ได้")
    else:
        for r in result:
            st.write(r)

