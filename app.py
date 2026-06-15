import re
from collections import defaultdict

def parse_order(text):
    data = defaultdict(lambda: {"บน": 0, "ล่าง": 0, "โต๊ด": 0})

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # 🔥 1. extract number
        m = re.match(r"^(\d{1,3})", line)
        if not m:
            continue
        n = m.group(1)

        # 🔥 2. extract price ONLY from * pattern OR last numbers
        if "*" in line:
            nums = [int(x) for x in re.findall(r"\d+", line)]
            # skip first number (id)
            price = nums[1:]
        else:
            # เอาเฉพาะเลขท้ายสุด ไม่เอาทั้งบรรทัด
            price = [int(x) for x in re.findall(r"\d+", line) if x != n]

        is_lower = "ล่าง" in line
        is_toe = "โต๊ด" in line

        # 🔥 3. MAP STRICTLY PER LINE (ห้าม aggregate ผิด channel)
        if len(price) == 1:
            if is_toe:
                data[n]["โต๊ด"] += price[0]
            elif is_lower:
                data[n]["ล่าง"] += price[0]
            else:
                data[n]["บน"] += price[0]

        elif len(price) == 2:
            if "บนล่าง" in line or "บน-ล่าง" in line:
                data[n]["บน"] += price[0]
                data[n]["ล่าง"] += price[1]
            elif is_lower and is_toe:
                data[n]["ล่าง"] += price[0]
                data[n]["โต๊ด"] += price[1]
            else:
                data[n]["บน"] += price[0]
                data[n]["ล่าง"] += price[1]

        elif len(price) == 3:
            data[n]["บน"] += price[0]
            data[n]["ล่าง"] += price[1]
            data[n]["โต๊ด"] += price[2]

    return [f"{k} {v['บน']} {v['ล่าง']} {v['โต๊ด']}" for k, v in data.items()]
