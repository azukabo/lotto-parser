import streamlit as st
import re
from collections import defaultdict

st.title("Lotto Parser (Rule Engine)")

def parse_line(line):
    parts = line.strip().split()
    if len(parts) < 2:
        return None

    number = parts[0]
    rest = parts[1:]

    # หา tag
    tag = None
    prices_part = []

    for p in rest:
        if p in ["บน", "ล่าง", "โต๊ด"]:
            tag = p
        else:
            prices_part.append(p)

    if not tag:
        tag = "บน"

    # parse price
    raw = prices_part[-1] if prices_part else ""
    nums = [int(x) for x in raw.split("*") if x.isdigit()]

    return number, tag, nums


def parse_order(text):
    data = defaultdict(lambda: {"บน": 0, "ล่าง": 0, "โต๊ด": 0})

    for line in text.split("\n"):
        parsed = parse_line(line)
        if not parsed:
            continue

        number, tag, nums = parsed

        if len(nums) == 1:
            data[number][tag] += nums[0]

        elif len(nums) == 2:
            if tag == "บน":
                data[number]["บน"] += nums[0]
                data[number]["ล่าง"] += nums[1]
            elif tag == "ล่าง":
                data[number]["ล่าง"] += nums[0]
            elif tag == "โต๊ด":
                data[number]["โต๊ด"] += nums[0]

        elif len(nums) == 3:
            data[number]["บน"] += nums[0]
            data[number]["ล่าง"] += nums[1]
            data[number]["โต๊ด"] += nums[2]

    return [f"{k} {v['บน']} {v['ล่าง']} {v['โต๊ด']}" for k, v in data.items()]


text = st.text_area("วางโพย")

if st.button("Parse"):
    st.text_area("Output", "\n".join(parse_order(text)), height=300)
