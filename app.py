import streamlit as st
import re

st.title("Lotto Parser")

def parse_order(text):
    results = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        is_lower = "ล่าง" in line
        is_toe = "โต๊ด" in line
        is_onoff = any(x in line for x in ["บนล่าง", "บน-ล่าง", "บน/ล่าง", "บน+ล่าง"])

        # price ดึงทุกแบบ 100*50 / 100 / 100*100*100
        price = []
        m = re.findall(r"\d+(?:\*\d+)*", line)
        if m:
            parts = m[-1].split("*")
            price = [int(x) for x in parts]

        # numbers = เลข 2-3 ตัว
        numbers = re.findall(r"\b\d{1,3}\b", line)
        numbers = [n for n in numbers if len(n) <= 3]

        if not price or not numbers:
            continue

        for n in numbers:
            if len(price) == 1:
                results.append(f"{n} {price[0]} 0 0")

            elif len(price) == 2:
                if is_lower and is_toe:
                    results.append(f"{n} 0 {price[0]} {price[1]}")
                elif is_onoff:
                    results.append(f"{n} {price[0]} {price[1]} 0")
                elif is_lower:
                    results.append(f"{n} 0 {price[0]} 0")
                elif is_toe:
                    results.append(f"{n} {price[0]} 0 {price[1]}")
                else:
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
