"""Draw the last 12 weeks of GitHub contributions as an LED station timetable (preview only)."""
import datetime as dt, json, subprocess, sys

OUT = sys.argv[1]
Q = '{user(login:"i-m-abbhay"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionCount}}}}}}'
cal = json.loads(subprocess.run(["gh", "api", "graphql", "-f", f"query={Q}"], capture_output=True, text=True, check=True).stdout)
cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = cal["weeks"][-12:]

MONO = "ui-monospace,SFMono-Regular,Consolas,Menlo,'Yu Gothic','Meiryo',monospace"
AMBER, DIM = "#ffb000", "#a8740a"
DAYS = [("SUN", "日"), ("MON", "月"), ("TUE", "火"), ("WED", "水"), ("THU", "木"), ("FRI", "金"), ("SAT", "土")]
X0, CW, Y0, RH = 130, 55, 120, 30

days = [d for w in weeks for d in w["contributionDays"]]
total12 = sum(d["contributionCount"] for d in days)
busiest = max(days, key=lambda d: d["contributionCount"])
peak = max(busiest["contributionCount"], 1)

s = [f"""<defs><pattern id="dots" width="3" height="3" patternUnits="userSpaceOnUse">
<rect x="2" width="1" height="3" fill="#000"/><rect y="2" width="3" height="1" fill="#000"/></pattern></defs>
<style>
.led{{font:700 14px {MONO};fill:{AMBER}}}
.h{{font:700 11px {MONO};fill:{DIM};letter-spacing:1px}}
.title{{font:800 20px {MONO};fill:{AMBER};letter-spacing:5px}}
.zero{{font:700 14px {MONO};fill:#2a2a2a}}
.today{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
</style>
<rect x="4" y="4" width="822" height="412" rx="14" fill="#16181b" stroke="#30363d" stroke-width="2"/>
<rect x="22" y="22" width="786" height="380" rx="6" fill="#050505"/>
<text x="40" y="56" class="title">TIMETABLE</text>
<text x="196" y="55" class="led" style="font-size:16px">時刻表</text>
<text x="790" y="55" text-anchor="end" class="h">TRAINS PER DAY = CONTRIBUTIONS · 1日の本数</text>"""]
for c, w in enumerate(weeks):
    start = dt.date.fromisoformat(w["contributionDays"][0]["date"])
    s.append(f'<text x="{X0 + c*CW + CW/2}" y="92" text-anchor="middle" class="h">{start.month}/{start.day}</text>')
for r, (en, ja) in enumerate(DAYS):
    y = Y0 + r * RH
    s.append(f'<text x="40" y="{y}" class="h">{en} {ja}</text>')
    s.append(f'<line x1="34" y1="{y+9}" x2="796" y2="{y+9}" stroke="#141414"/>')
last_date = days[-1]["date"]
for c, w in enumerate(weeks):
    for d in w["contributionDays"]:
        n, y = d["contributionCount"], Y0 + d["weekday"] * RH
        cx = X0 + c * CW + CW / 2
        if n:
            alpha = 0.12 + 0.55 * n / peak
            s.append(f'<rect x="{cx-22}" y="{y-16}" width="44" height="22" rx="3" fill="{AMBER}" opacity="{alpha:.2f}"/>')
        cls = "led" if n else "zero"
        if d["date"] == last_date:
            cls += " today"
        s.append(f'<text x="{cx}" y="{y}" text-anchor="middle" class="{cls}">{n if n else "--"}</text>')
b = dt.date.fromisoformat(busiest["date"])
s.append(f"""<line x1="22" y1="338" x2="808" y2="338" stroke="#2a2a2a"/>
<text x="40" y="364" class="led">LAST 12 WEEKS: {total12} trains · 直近12週: {total12}本</text>
<text x="40" y="388" class="led" style="fill:{DIM}">THIS YEAR: {cal['totalContributions']} · BUSIEST: {b:%b %d} ({busiest['contributionCount']}) · 最多: {b.month}月{b.day}日</text>
<rect x="22" y="22" width="786" height="380" rx="6" fill="url(#dots)" opacity=".45"/>""")
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 420" width="830" height="420">\n' + "\n".join(s) + "\n</svg>\n"
open(OUT, "w", encoding="utf-8", newline="\n").write(svg)
print("ok", total12, cal["totalContributions"])
