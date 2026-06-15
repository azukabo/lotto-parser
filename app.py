import streamlit as st
import re

st.title("Lotto Parser")

def parse_order(text):
    data = {}

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^(\d{1,3})", line)
        if not m:
            continue

        n = m.group(1)

        if n not in data:
            data[n] = {"บน": 0, "ล่าง": 0, "โต๊ด": 0}

        nums = re.findall(r"\d+", line)
        if len(nums) < 2:
            continue

        price = int(nums[-1])  # 🔥 FIX: ใช้ตัวท้ายสุดเท่านั้น (stable)

        # 🔥 PRIORITY RULE (สำคัญสุด)
        if "โต๊ด" in line:
            data[n]["โต๊ด"] += price

        elif "บนล่าง" in line or "บน-ล่าง" in line:
            data[n]["บน"] += price
            data[n]["ล่าง"] += price

        elif "ล่าง" in line:
            data[n]["ล่าง"] += price

        else:
            data[n]["บน"] += price

    return [f"{k} {v['บน']} {v['ล่าง']} {v['โต๊ด']}" for k, v in data.items()]


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    st.text_area("Output", "\n".join(parse_order(text)), height=300)
