import streamlit as st
import re

st.title("Lotto Parser")

mode = st.radio("Mode", ["Merge", "Split"])

def parse_order(text, mode="Merge"):
    results = {}

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^\s*(\d{1,3})", line)
        if not m:
            continue
        n = m.group(1)

        is_lower = "ล่าง" in line
        is_toe = "โต๊ด" in line

        price_match = re.findall(r"\d+(?:\*\d+)*", line)
        if not price_match:
            continue

        last = price_match[-1]
        price = [int(x) for x in last.split("*")] if "*" in last else [int(last)]

        if n not in results:
            results[n] = {"บน": 0, "ล่าง": 0, "โต๊ด": 0}

        if len(price) == 1:
            results[n]["บน"] += price[0]

        elif len(price) == 2:
            if is_lower and is_toe:
                results[n]["ล่าง"] += price[0]
                results[n]["โต๊ด"] += price[1]
            elif is_lower:
                results[n]["ล่าง"] += price[0]
            elif is_toe:
                results[n]["โต๊ด"] += price[0]
            else:
                results[n]["บน"] += price[0]
                results[n]["ล่าง"] += price[1]

        elif len(price) == 3:
            results[n]["บน"] += price[0]
            results[n]["ล่าง"] += price[1]
            results[n]["โต๊ด"] += price[2]

    output = []

    if mode == "Merge":
        for n, v in results.items():
            output.append(f"{n} {v['บน']} {v['ล่าง']} {v['โต๊ด']}")

    else:  # Split
        for n, v in results.items():
            if v["บน"]:
                output.append(f"{n} {v['บน']} 0 0")
            if v["ล่าง"]:
                output.append(f"{n} 0 {v['ล่าง']} 0")
            if v["โต๊ด"]:
                output.append(f"{n} 0 0 {v['โต๊ด']}")

    return output


text = st.text_area("วางโพยที่นี่")

if st.button("Parse"):
    result = parse_order(text, mode)

    st.text_area("Output", "\n".join(result), height=250)
