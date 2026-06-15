import streamlit as st
import re

st.title("Lotto Parser")

def parse_order(text):
    results = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^(\d{1,3})", line)
        if not m:
            continue

        n = m.group(1)

        nums = re.findall(r"\d+", line)

        # กัน crash
        if len(nums) < 2:
            continue

        price = nums[1:]

        # convert safe
        try:
            price = [int(x) for x in price]
        except:
            continue

        # safe output only (ยังไม่ logic ซับซ้อน)
        if len(price) == 1:
            results.append(f"{n} {price[0]} 0 0")
        elif len(price) == 2:
            results.append(f"{n} {price[0]} {price[1]} 0")
        elif len(price) == 3:
            results.append(f"{n} {price[0]} {price[1]} {price[2]}")

    return results


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    st.text_area("Output", "\n".join(parse_order(text)), height=300)
