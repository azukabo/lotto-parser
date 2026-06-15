def parse_order(text):
    import re

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

        # 🔥 FIX CORE: handle * properly
        price_part = re.findall(r"\d+(?:\*\d+)*", line)
        if not price_part:
            continue

        raw = price_part[-1]

        if "*" in raw:
            p = [int(x) for x in raw.split("*")]
        else:
            p = [int(raw)]

        # 🔥 TAG priority
        if "โต๊ด" in line:
            data[n]["โต๊ด"] += p[0]

        elif "บนล่าง" in line or "บน-ล่าง" in line:
            if len(p) == 2:
                data[n]["บน"] += p[0]
                data[n]["ล่าง"] += p[1]
            continue

        elif "ล่าง" in line:
            data[n]["ล่าง"] += p[0]

        else:
            # 🔥 FIX HERE (IMPORTANT)
            if len(p) == 1:
                data[n]["บน"] += p[0]
            elif len(p) == 2:
                data[n]["บน"] += p[0]
                data[n]["ล่าง"] += p[1]
            elif len(p) == 3:
                data[n]["บน"] += p[0]
                data[n]["ล่าง"] += p[1]
                data[n]["โต๊ด"] += p[2]

    return [f"{k} {v['บน']} {v['ล่าง']} {v['โต๊ด']}" for k, v in data.items()]
