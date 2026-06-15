import streamlit as st
import re

st.title("Lotto Parser")

def parse_order(text):
    results = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # ดึงเลขตัวแรก (กันมั่ว)
        m = re.match(r"^\s*(\d{1,3})", line)
        if not m:
            continue
        n = m.group(1)

        # ดึงราคา
        price_match = re.findall(r"\d+(?:\*\d+)*", line)
        if not price_match:
            continue

        last = price_match[-1]
        price = [int(x) for x in last.split("*")] if "*" in last else [int(last)]

        # default mapping ก่อน (ปลอดภัยสุด)
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
    st.write(result)
