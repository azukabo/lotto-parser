import streamlit as st
import re
import streamlit.components.v1 as components

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

        # 💰 ราคา
        price_match = re.findall(r"\d+(?:\*\d+)+|\d+", line)
        price = None

        if price_match:
            last = price_match[-1]
            if "*" in last:
                price = [int(x) for x in last.split("*")]
            elif last.isdigit() and len(last) > 1:
                price = [int(last)]

        # 🎯 เลขแทง = เอา "ตัวแรกของบรรทัด" เท่านั้น
        first_numbers = re.findall(r"^\s*(\d{1,3})", line)
        if not first_numbers:
            continue

        n = first_numbers[0]

        if not price:
            continue

        # logic mapping
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

    if result:
        output_text = "\n".join(result)

        st.subheader("ผลลัพธ์")

        st.text_area("Output", output_text, height=250)

        copy_html = f"""
        <button onclick="navigator.clipboard.writeText(`{output_text}`)"
        style="padding:10px 20px;font-size:16px;">
        📋 Copy
        </button>
        """

        components.html(copy_html, height=60)

    else:
        st.warning("ไม่มีข้อมูลที่ parse ได้")
