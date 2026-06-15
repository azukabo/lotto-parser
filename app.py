import streamlit as st
import re

st.title("Lotto Parser")

def parse_order(text):
    results = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # หา price เช่น 100*100 หรือ 200*200*200
        price_match = re.findall(r"\d+\*\d+(?:\*\d+)?", line)
        if not price_match:
            continue

        price = [int(x) for x in price_match[0].split("*")]

        tokens = line.split()
        numbers = [t for t in tokens if t.isdigit() and len(t) <= 3]

        is_lower = "ล่าง" in line
        is_toe = "โต๊ด" in line
        is_onoff = any(x in line for x in ["บนล่าง", "บน-ล่าง", "บน/ล่าง", "บน+ล่าง"])
        is_full = "บนล่างโต๊ด" in line

        for n in numbers:
            if len(n) == 2:
                results.append(f"{n} {price[0]} {price[1]} 0")
            else:
                if len(price) == 3:
                    results.append(f"{n} {price[0]} {price[1]} {price[2]}")
                elif is_full:
                    results.append(f"{n} {price[0]} {price[1]} {price[2]}")
                elif is_lower and is_toe:
                    results.append(f"{n} 0 {price[0]} {price[1]}")
                elif is_onoff:
                    results.append(f"{n} {price[0]} {price[1]} 0")
                elif is_lower:
                    results.append(f"{n} 0 {price[0]} 0")
                elif is_toe:
                    results.append(f"{n} {price[0]} 0 {price[1]}")
                else:
                    results.append(f"{n} {price[0]} 0 {price[1]}")

    return results


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    result = parse_order(text)

    st.subheader("ผลลัพธ์")
    for r in result:
        st.write(r)
