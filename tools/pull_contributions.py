import json
import re
from datetime import datetime, timezone
from urllib.request import Request, urlopen

USERNAME = "Yuvaraj187"
URL = f"https://github.com/users/{USERNAME}/contributions"

req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urlopen(req, timeout=30) as response:
    html = response.read().decode("utf-8", errors="ignore")

pattern = re.compile(r'<td[^>]*data-date=["\']([^"\']+)["\'][^>]*data-level=["\']([0-4])["\'][^>]*>', re.I)
items = [{"date": d, "level": int(level)} for d, level in pattern.findall(html)]

if not items:
    # Newer/alternate markup: find the attributes independently within each cell.
    cells = re.findall(r'<td\b[^>]*>.*?</td>', html, flags=re.I | re.S)
    for cell in cells:
        dm = re.search(r'data-date=["\']([^"\']+)', cell, re.I)
        lm = re.search(r'data-level=["\']([0-4])', cell, re.I)
        if dm and lm:
            items.append({"date": dm.group(1), "level": int(lm.group(1))})

items.sort(key=lambda x: x["date"])
counts = [x["level"] for x in items]
total = sum(counts)

# The HTML exposes levels rather than exact counts in all renderings, so keep a compact
# level-based dataset for the custom graph. The raw HTML remains the source of truth.
output = {
    "username": USERNAME,
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "total_level_sum": total,
    "days": items,
}

with open("assets/contributions.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(items)} contribution cells to assets/contributions.json")
