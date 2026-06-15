def parse_order(text):
    results = []
    seen = set()

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        is_lower = "ล่าง" in line
        is_toe = "โต๊ด" in line
        is_onoff = any(x in line for x in ["บนล่าง", "บน-ล่าง", "บน/ล่าง", "บน+ล่าง"])

        price_match = re.findall(r"\d+(?:\*\d+)*", line)
        if not price_match:
            continue

        last = price_match[-1]
        price = [int(x) for x in last.split("*")] if "*" in last else [int(last)]

        m = re.match(r"^\s*(\d{1,3})", line)
        if not m:
            continue

        n = m.group(1)

        # 🔥 dedupe key (สำคัญ)
        key = (n, tuple(price), is_lower, is_toe, is_onoff)
        if key in seen:
            continue
        seen.add(key)

        if len(price) == 1:
            results.append(f"{n} {price[0]} 0 0")

        elif len(price) == 2:
            if is_lower and is_toe:
                results.append(f"{n} 0 {price[0]} {price[1]}")
            elif is_onoff:
                results.append(f"{n} {price[0]} {price[1]} 0")
            elif is_lower:
                results.append(f"{n} 0 {price[0]} 0")
            elif is_toe:
                results.append(f"{n} {price[0]} 0 {price[1]}")
            else:
                results.append(f"{n} {price[0]} {price[1]} 0")

        elif len(price) == 3:
            results.append(f"{n} {price[0]} {price[1]} {price[2]}")

    return results
