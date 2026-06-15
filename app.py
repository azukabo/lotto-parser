import streamlit as st
import re

st.title("Lotto Parser")

def parse_order(text):
    out = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^(\d{1,3})", line)
        if not m:
            continue

        n = m.group(1)

        # ดึงเลขทั้งหมดในบรรทัด
        nums = re.findall(r"\d+", line)

        if len(nums) < 2:
            continue

        # เอาทุกตัวหลังเลขแรก (ยังไม่ตีความซับซ้อน)
        price = [int(x) for x in nums[1:]]

        if len(price) == 1:
            out.append(f"{n} {price[0]} 0 0")
        elif len(price) == 2:
            out.append(f"{n} {price[0]} {price[1]} 0")
        elif len(price) == 3:
            out.append(f"{n} {price[0]} {price[1]} {price[2]}")

    return out


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    st.text_area("Output", "\n".join(parse_order(text)), height=300)
