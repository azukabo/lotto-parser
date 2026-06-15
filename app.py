import streamlit as st
import re
from collections import defaultdict

st.title("Lotto Parser 🔒 LOCKED")

def extract_price(line):
    # เอาเฉพาะ pattern ตัวเลข*ตัวเลข หรือ ตัวเลขเดี่ยวท้ายสุด
    parts = re.findall(r"\d+(?:\*\d+)*", line)
    if not parts:
        return None

    last = parts[-1]

    if "*" in last:
        return [int(x) for x in last.split("*")]

    # กันเคสเลขมั่วติดกัน (เช่น 200 200 200)
    nums = re.findall(r"\d+", line)
    if len(nums) >= 2 and "*" not in line:
        # ใช้แค่ 1-2 ตัวแรกเท่านั้น (กัน 123 100 100 100 พัง)
        return [int(nums[-1])]

    return [int(last)]


def parse_order(text):
    data = defaultdict(lambda: {"บน": 0, "ล่าง": 0, "โต๊ด": 0})

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # 🔒 FIX 1: number must be FIRST token only
        m = re.match(r"^(\d{1,3})", line)
        if not m:
            continue

        n = m.group(1)

        price = extract_price(line)
        if not price:
            continue

        is_lower = "ล่าง" in line
        is_toe = "โต๊ด" in line
        is_split = "บนล่าง" in line or "บน-ล่าง" in line

        # 🔒 RULE ENGINE (fixed only)
        if len(price) == 1:
            data[n]["บน"] += price[0]

        elif len(price) == 2:
            if is_split:
                data[n]["บน"] += price[0]
                data[n]["ล่าง"] += price[1]
            elif is_lower and is_toe:
                data[n]["ล่าง"] += price[0]
                data[n]["โต๊ด"] += price[1]
            elif is_lower:
                data[n]["ล่าง"] += price[0]
            elif is_toe:
                data[n]["โต๊ด"] += price[0]
            else:
                data[n]["บน"] += price[0]
                data[n]["ล่าง"] += price[1]

        elif len(price) == 3:
            data[n]["บน"] += price[0]
            data[n]["ล่าง"] += price[1]
            data[n]["โต๊ด"] += price[2]

    return [f"{k} {v['บน']} {v['ล่าง']} {v['โต๊ด']}" for k, v in data.items()]


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    st.text_area("Output", "\n".join(parse_order(text)), height=300)
