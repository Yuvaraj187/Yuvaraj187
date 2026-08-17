import json
from pathlib import Path

DATA = Path("assets/contributions.json")
OUT = Path("assets/graph.svg")

with DATA.open(encoding="utf-8") as f:
    payload = json.load(f)

days = {x["date"]: x["level"] for x in payload.get("days", [])}
ordered = sorted(days.items())[-371:]

# Arrange into seven-day columns. This deliberately stays dependency-free for Actions.
while len(ordered) % 7:
    ordered.insert(0, ("", 0))

cols = [ordered[i:i+7] for i in range(0, len(ordered), 7)]
cell = 12
gap = 4
left, top = 45, 70
width = left * 2 + len(cols) * (cell + gap)
height = 225

colors = ["#101722", "#12311f", "#145a2d", "#16853e", "#39e86f"]
parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
<defs><style>
.bg{{fill:#080d14}}.t{{fill:#8b98aa;font-family:monospace}}.h{{fill:#dce6f2;font-family:monospace;font-weight:700}}
.c{{opacity:0;animation:reveal .45s ease forwards}}@keyframes reveal{{to{{opacity:1}}}}
</style></defs><rect class="bg" width="100%" height="100%" rx="8"/>
<text x="24" y="27" class="h" font-size="14">$ contributions --live</text>
<text x="24" y="48" class="t" font-size="11">Yuvaraj187 · generated from GitHub contribution activity</text>''']

for col_idx, col in enumerate(cols):
    delay = min(col_idx * 0.025, 1.8)
    parts.append(f'<g class="c" style="animation-delay:{delay:.3f}s">')
    for row_idx, (_, level) in enumerate(col):
        x = left + col_idx * (cell + gap)
        y = top + row_idx * (cell + gap)
        parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{colors[level]}"/>')
    parts.append('</g>')

parts.append(f'''<g transform="translate({left} {top + 7*{cell+gap} + 10})">''')
for i, color in enumerate(colors):
    parts.append(f'<rect x="{i*22}" y="0" width="13" height="13" rx="3" fill="{color}"/>')
parts.append('<text x="120" y="11" class="t" font-size="10">less</text><text x="100%" y="11" class="t" font-size="10" text-anchor="end">more</text></g></svg>')

OUT.write_text("".join(parts), encoding="utf-8")
print(f"Rendered {len(cols)} weeks to {OUT}")
