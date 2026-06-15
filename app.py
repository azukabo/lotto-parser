def parse_order(text):
    from collections import defaultdict
    data = defaultdict(lambda: {"บน": 0, "ล่าง": 0, "โต๊ด": 0})

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^\s*(\d{1,3})", line)
        if not m:
            continue
        n = m.group(1)

        price_match = re.findall(r"\d+(?:\*\d+)*", line)
        if not price_match:
            continue

        last = price_match[-1]
        price = [int(x) for x in last.split("*")] if "*" in last else [int(last)]

        # 🔥 KEY FIX: "บนล่าง" = split เป็น (บน, ล่าง)
        if "บนล่าง" in line or "บน-ล่าง" in line or "บน/ล่าง" in line or "บน+ล่าง" in line:
            if len(price) == 2:
                data[n]["บน"] += price[0]
                data[n]["ล่าง"] += price[1]
            continue

        if "ล่าง" in line and "โต๊ด" in line:
            if len(price) == 2:
                data[n]["ล่าง"] += price[0]
                data[n]["โต๊ด"] += price[1]
            continue

        if "ล่าง" in line:
            data[n]["ล่าง"] += price[0]
            continue

        if "โต๊ด" in line:
            data[n]["โต๊ด"] += price[0]
            continue

        # default = บน
        if len(price) == 1:
            data[n]["บน"] += price[0]
        elif len(price) == 2:
            data[n]["บน"] += price[0]
            data[n]["ล่าง"] += price[1]
        elif len(price) == 3:
            data[n]["บน"] += price[0]
            data[n]["ล่าง"] += price[1]
            data[n]["โต๊ด"] += price[2]

    return [f"{k} {v['บน']} {v['ล่าง']} {v['โต๊ด']}" for k, v in data.items()]
