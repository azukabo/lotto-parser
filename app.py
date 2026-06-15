def parse_order(text):
    import re
    from collections import defaultdict

    data = defaultdict(lambda: {"บน": 0, "ล่าง": 0, "โต๊ด": 0})

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^(\d{1,3})", line)
        if not m:
            continue

        n = m.group(1)

        nums = re.findall(r"\d+", line)
        if len(nums) < 2:
            continue

        # price parsing (safe)
        raw_prices = nums[1:]
        price = [int(x) for x in raw_prices]

        # ---------------- RULE ENGINE ----------------
        is_lower = "ล่าง" in line
        is_toe = "โต๊ด" in line
        is_split = "บนล่าง" in line or "บน-ล่าง" in line

        # 1 number
        if len(price) == 1:
            if is_toe:
                data[n]["โต๊ด"] += price[0]
            elif is_lower:
                data[n]["ล่าง"] += price[0]
            else:
                data[n]["บน"] += price[0]

        # 2 numbers
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

        # 3 numbers
        elif len(price) == 3:
            data[n]["บน"] += price[0]
            data[n]["ล่าง"] += price[1]
            data[n]["โต๊ด"] += price[2]

    return [f"{k} {v['บน']} {v['ล่าง']} {v['โต๊ด']}" for k, v in data.items()]
