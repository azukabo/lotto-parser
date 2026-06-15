import streamlit as st
import re

st.set_page_config(page_title="Lotto Parser", layout="centered")

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
        is_full = "บนล่างโต๊ด" in line

        # ดึงราคา (100*50 / 100 / 100*100*100)
        price = []
        price_match = re.findall(r"\d+(?:\*\d+)*", line)
        if price_match:
            parts = price_match[-1].split("*")
            price = [int(x) for x in parts]

        # ดึงเลข 2-3 ตัว
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


text = st.text_area("วางโพยที่นี่ (จาก LINE ได้เลย)")

if st.button("Parse"):
    result = parse_order(text)

    st.subheader("ผลลัพธ์")

    if result:
        output_text = "\n".join(result)

        st.text_area("📋 Copy ได้เลย", output_text, height=250)

        st.download_button(
            label="⬇️ Download TXT",
            data=output_text,
            file_name="lotto_result.txt",
            mime="text/plain"
        )

    else:
        st.warning("ไม่มีข้อมูลที่ parse ได้")
