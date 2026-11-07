"""Generate the railway-themed SVGs for the GitHub profile README."""
import os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI',-apple-system,Helvetica,Arial,'Hiragino Sans','Yu Gothic UI','Meiryo','Noto Sans JP',sans-serif"
JP = "'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic UI','Yu Gothic','Meiryo','Noto Sans JP',sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,Menlo,'Liberation Mono',monospace"
TEAL = "#0e7c66"


def save(name, body, w, h):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n{body}\n</svg>\n'
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


# 1. Station name sign
save("header.svg", f"""<style>
.jp{{font:700 58px {JP};fill:#1b1f24}}
.en{{font:600 21px {SANS};fill:#1b1f24;letter-spacing:7px}}
.side{{font:600 15px {SANS};fill:#fff}}
.sidejp{{font:700 12px {JP};fill:#cdeee6}}
.sub{{font:500 13px {SANS};fill:#57606a}}
.next{{animation:nudge 1.6s ease-in-out infinite}}
@keyframes nudge{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(5px)}}}}
</style>
<rect x="4" y="4" width="822" height="242" rx="14" fill="#fff" stroke="#d0d7de" stroke-width="2"/>
<rect x="34" y="30" width="64" height="64" rx="10" fill="#fff" stroke="{TEAL}" stroke-width="5"/>
<text x="66" y="56" text-anchor="middle" style="font:700 15px {SANS};fill:{TEAL}">AT</text>
<text x="66" y="83" text-anchor="middle" style="font:800 24px {SANS};fill:#1b1f24">24</text>
<text x="415" y="94" text-anchor="middle" class="jp">ティワリアブハイ</text>
<text x="415" y="128" text-anchor="middle" class="en">ABHAY TIWARI</text>
<rect x="5" y="148" width="820" height="50" fill="{TEAL}"/>
<circle cx="415" cy="173" r="12" fill="#fff" stroke="#1b1f24" stroke-width="4"/>
<polygon points="30,173 42,165 42,181" fill="#fff"/>
<text x="52" y="168" class="sidejp">ダンバード</text>
<text x="52" y="188" class="side">Dhanbad · IIT (ISM) 2024</text>
<g class="next">
<text x="778" y="168" text-anchor="end" class="sidejp">つぎ</text>
<text x="778" y="188" text-anchor="end" class="side">next-idea</text>
<polygon points="800,173 788,165 788,181" fill="#fff"/>
</g>
<text x="415" y="226" text-anchor="middle" class="sub">Software Development Engineer at Standard Force  ·  長崎県大村市  Omura, Nagasaki, Japan</text>""", 830, 250)


# 2. Life route with a moving train (from LinkedIn)
stations = [
    ("2020", "IIT (ISM) Dhanbad", ["B.Tech begins"]),
    ("2021", "Graphic designer", ["film posters,", "freelance brands"]),
    ("2022", "NVCTI, Dhanbad", ["Innovation Cell", "coordinator"]),
    ("2023", "LTU Corporation", ["full-stack intern,", "remote for Japan"]),
    ("2024", "Standard Force", ["SDE in Omura,", "Nagasaki"]),
    ("NEXT", "next-idea", ["boarding soon"]),
]
xs = [80, 214, 348, 482, 616, 750]
CUR = 4
LY = 132
now = [
    "NOW AT STANDARD FORCE:  RabbitMQ notification system across chat platforms  ·  seismic assessment platform, 10× faster",
    "KPI dashboard on the ERP  ·  PyQt + SQLite app over 2M+ records  ·  Grafana, Prometheus and Loki across 8 servers",
]
parts = [f"""<style>
.t{{font:700 13px {SANS};fill:#8b949e;letter-spacing:3px}}
.tj{{font:700 13px {JP};fill:#6e7681}}
.y{{font:700 12px {MONO};fill:#f5a524;letter-spacing:1px}}
.n{{font:700 13px {SANS};fill:#e6edf3}}
.d{{font:400 12px {SANS};fill:#8b949e}}
.here{{font:700 12px {SANS};fill:#f5a524}}
.now{{font:500 12px {SANS};fill:#c9d1d9}}
.train{{animation:ride 8s cubic-bezier(.45,0,.25,1) infinite}}
@keyframes ride{{0%{{transform:translateX(0)}}75%,100%{{transform:translateX({xs[CUR]-xs[0]}px)}}}}
.pulse{{transform-origin:{xs[CUR]}px {LY}px;animation:pulse 2s ease-out infinite}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.8}}100%{{transform:scale(2.6);opacity:0}}}}
</style>
<rect x="4" y="4" width="822" height="292" rx="14" fill="#0f141a" stroke="#30363d" stroke-width="2"/>
<text x="34" y="42" class="t">THE ROUTE SO FAR</text>
<text x="796" y="42" text-anchor="end" class="tj">これまでの路線</text>
<line x1="{xs[0]}" y1="{LY}" x2="{xs[CUR]}" y2="{LY}" stroke="{TEAL}" stroke-width="8" stroke-linecap="round"/>
<line x1="{xs[CUR]}" y1="{LY}" x2="{xs[-1]}" y2="{LY}" stroke="#484f58" stroke-width="6" stroke-dasharray="4 8" stroke-linecap="round"/>
<circle class="pulse" cx="{xs[CUR]}" cy="{LY}" r="10" fill="none" stroke="#f5a524" stroke-width="3"/>"""]
for i, (x, (year, name, lines)) in enumerate(zip(xs, stations)):
    last = i == len(xs) - 1
    fill, stroke = ("#0f141a", "#484f58") if last else ("#fff", "#1b1f24")
    parts.append(f'<circle cx="{x}" cy="{LY}" r="10" fill="{fill}" stroke="{stroke}" stroke-width="4"/>')
    parts.append(f'<text x="{x}" y="{LY-44}" text-anchor="middle" class="y">{year}</text>')
    parts.append(f'<text x="{x}" y="{LY-24}" text-anchor="middle" class="n">{name}</text>')
    lines = lines + (["you are here"] if i == CUR else [])
    for j, line in enumerate(lines):
        cls = "here" if line == "you are here" else "d"
        parts.append(f'<text x="{x}" y="{LY+34+j*17}" text-anchor="middle" class="{cls}">{line}</text>')
parts.append(f"""<g class="train">
<rect x="{xs[0]-22}" y="{LY-10}" width="44" height="20" rx="7" fill="#f5a524" stroke="#0f141a" stroke-width="2"/>
<rect x="{xs[0]-14}" y="{LY-5}" width="8" height="7" rx="1.5" fill="#0f141a"/>
<rect x="{xs[0]-3}" y="{LY-5}" width="8" height="7" rx="1.5" fill="#0f141a"/>
<rect x="{xs[0]+8}" y="{LY-5}" width="8" height="7" rx="1.5" fill="#0f141a"/>
</g>
<line x1="34" y1="230" x2="796" y2="230" stroke="#30363d"/>
<text x="415" y="256" text-anchor="middle" class="now">{now[0]}</text>
<text x="415" y="276" text-anchor="middle" class="now">{now[1]}</text>""")
save("journey.svg", "\n".join(parts), 830, 300)


# 3. LED departures board for projects (alternates English / Japanese like real station boards)
AMBER, DIM = "#ffb000", "#a8740a"
MONO_JP = MONO + ",'Yu Gothic','Meiryo','Hiragino Sans','Noto Sans JP'"
SWAP = """.en{animation:en 8s infinite}.ja{animation:ja 8s infinite}
@keyframes en{0%,44%{opacity:1}50%,94%{opacity:0}100%{opacity:1}}
@keyframes ja{0%,44%{opacity:0}50%,94%{opacity:1}100%{opacity:0}}
.blink{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}"""
DOTS = """<pattern id="dots" width="3" height="3" patternUnits="userSpaceOnUse">
<rect x="2" width="1" height="3" fill="#000"/><rect y="2" width="3" height="1" fill="#000"/>
</pattern>"""


def bi(x, y, cls, en, ja, extra=""):
    """Same spot, English then Japanese, crossfading."""
    return (f'<text x="{x}" y="{y}" class="{cls} en"{extra}>{en}</text>'
            f'<text x="{x}" y="{y}" class="{cls} ja"{extra}>{ja}</text>')


R = ' text-anchor="end"'
rows = [
    ("09:00", ("Rapid", "快速"), "#ff7b72", "pounce", ("pixel pet for Claude Code", "Claude Code用ピクセルペット"), ("BOARDING", "乗車中"), "#3ddc84", True),
    ("09:12", ("Express", "急行"), "#ffd166", "direct4b-mcp", ("MCP server for team chat", "チームチャット用MCPサーバー"), ("On time", "定刻"), AMBER, False),
    ("09:30", ("Local", "普通"), "#79c0ff", "nihongo", ("learn Japanese by building", "作りながら日本語を学ぶ"), ("On time", "定刻"), AMBER, False),
    ("09:48", ("Local", "普通"), "#79c0ff", "karimen-honmen", ("driving test practice", "運転免許の試験対策"), ("On time", "定刻"), AMBER, False),
    ("10:05", ("Local", "普通"), "#79c0ff", "Eat-That-Frog", ("task tracker", "タスク管理"), ("Delayed: procrastinating", "遅延：先延ばし中"), "#ff7b72", False),
]
ticker = ("Thank you for visiting.    ご覧いただきありがとうございます。    次は next-idea です。    "
          "Please mind the gap between learning and shipping.    学びと出荷のすき間にご注意ください。")
p = [f"""<defs>{DOTS}
<clipPath id="band"><rect x="22" y="290" width="786" height="34"/></clipPath>
</defs>
<style>
.led{{font:700 16px {MONO_JP};fill:{AMBER}}}
.via{{font:600 13px {MONO_JP};fill:{DIM}}}
.h{{font:700 12px {MONO_JP};fill:{DIM};letter-spacing:2px}}
.title{{font:800 20px {MONO};fill:{AMBER};letter-spacing:5px}}
.titlejp{{font:700 16px {JP};fill:{AMBER}}}
{SWAP}
.tick{{animation:tick 34s linear infinite}}
@keyframes tick{{0%{{transform:translateX(0)}}100%{{transform:translateX(-2300px)}}}}
</style>
<rect x="4" y="4" width="822" height="332" rx="14" fill="#16181b" stroke="#30363d" stroke-width="2"/>
<rect x="22" y="22" width="786" height="300" rx="6" fill="#050505"/>
<text x="40" y="56" class="title">DEPARTURES</text>
<text x="208" y="55" class="titlejp">発車案内</text>
{bi(790, 55, "h", "PLATFORM: main", "のりば: main", R)}
{bi(40, 88, "h", "TIME", "時刻")}{bi(112, 88, "h", "TYPE", "種別")}
{bi(210, 88, "h", "DESTINATION", "行先")}{bi(790, 88, "h", "STATUS", "備考", R)}
<line x1="34" y1="98" x2="796" y2="98" stroke="#2a2a2a"/>"""]
for i, (t, typ, tcol, dest, via, status, scol, blink) in enumerate(rows):
    y = 124 + i * 34
    p.append(f'<text x="40" y="{y}" class="led">{t}</text>')
    p.append(bi(112, y, "led", *typ, f' style="fill:{tcol}"'))
    p.append(f'<text x="210" y="{y}" class="led">{dest}</text>')
    p.append(bi(210 + len(dest) * 10 + 14, y, "via", *via))
    st = bi(790, y, "led", *status, f'{R} style="fill:{scol}"')
    p.append(f'<g class="blink">{st}</g>' if blink else st)
    p.append(f'<line x1="34" y1="{y+11}" x2="796" y2="{y+11}" stroke="#1a1a1a"/>')
p.append(f"""<line x1="22" y1="290" x2="808" y2="290" stroke="#2a2a2a"/>
<g clip-path="url(#band)"><g class="tick">
<text x="808" y="313" class="led">{ticker}</text>
</g></g>
<rect x="22" y="22" width="786" height="300" rx="6" fill="url(#dots)" opacity=".45"/>""")
save("departures.svg", "\n".join(p), 830, 340)


# 4. Tech stack as a transit map: trunk + branches + transfer passages
LINES = {
    "L": ("#f5a524", "Languages", "言語線"),
    "F": ("#2bb3a3", "Frontend", "フロント線"),
    "B": ("#ff7b72", "Backend", "バックエンド線"),
    "D": ("#58a6ff", "Data", "データ線"),
    "O": ("#d16ba5", "Ops", "運用線"),
}
TY, FY, BY, DY = 210, 130, 300, 390
trunk = [("JavaScript", 100), ("TypeScript", 220), ("PHP", 340), ("Python", 470), ("Go", 600), ("C++", 720)]
front = [("React", 300), ("Next.js", 390), ("Vue", 480), ("Svelte", 570), ("Tailwind", 660)]
back = [("Node.js", 100), ("Express", 175), ("Laravel", 340), ("Django", 470), ("FastAPI", 535), ("Gin", 600)]
data = [("MySQL", 100), ("PostgreSQL", 190), ("MongoDB", 280), ("SQLite", 370)]
ops = [("Docker", 470), ("RabbitMQ", 530), ("Grafana", 590), ("Prometheus", 650), ("Loki", 710), ("Git", 770)]
transfers = [100, 340, 470, 600]  # language station <-> its backend framework


def path(d, col):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'


def stop(x, y, big=False):
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="#0f141a" stroke-width="4"/>' if big
            else f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="#0f141a" stroke-width="3"/>')


def label(x, y, name, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="st">{name}</text>'


m = [f"""<style>
.t{{font:700 13px {SANS};fill:#8b949e;letter-spacing:3px}}
.tj{{font:700 13px {JP};fill:#6e7681}}
.st{{font:600 12px {SANS};fill:#e6edf3}}
.b{{font:800 12px {SANS};fill:#0f141a}}
.lg{{font:600 12px {SANS};fill:#c9d1d9}}
.lgj{{font:500 11px {JP};fill:#8b949e}}
.water{{font:italic 500 11px {SANS};fill:#2d4a5e;letter-spacing:4px}}
</style>
<rect x="4" y="4" width="822" height="476" rx="14" fill="#0f141a" stroke="#30363d" stroke-width="2"/>
<path d="M5,70 C70,60 140,92 190,78 C200,110 170,150 120,160 C80,168 40,150 5,158 Z" fill="#12202b"/>
<text x="95" y="120" text-anchor="middle" class="water">OMURA BAY</text>
<text x="95" y="138" text-anchor="middle" class="water">大村湾</text>
<text x="34" y="42" class="t">NETWORK MAP</text>
<text x="796" y="42" text-anchor="end" class="tj">路線図</text>"""]
# transfer passages (drawn first, under the lines)
for x in transfers:
    m.append(f'<rect x="{x-5}" y="{TY}" width="10" height="{BY-TY}" fill="#0f141a" stroke="#8b949e" stroke-width="2"/>')
# lines
m.append(path(f"M60,{TY} H770", LINES["L"][0]))
m.append(path(f"M220,{TY} V{FY+22} Q220,{FY} 242,{FY} H700", LINES["F"][0]))
m.append(path(f"M70,{BY} H630", LINES["B"][0]))
m.append(path(f"M70,{DY} H400", LINES["D"][0]))
m.append(path(f"M440,{DY} H790", LINES["O"][0]))
# stations + labels
for name, x in trunk:
    m.append(stop(x, TY, big=x in transfers or x == 220))
    if x == 220:
        m.append(label(208, TY - 16, name, "end"))
    else:
        m.append(label(x, TY - 18, name))
for name, x in front:
    m.append(stop(x, FY))
    m.append(label(x, FY - 16, name))
for name, x in back:
    m.append(stop(x, BY, big=x in transfers))
    m.append(label(x, BY + 28, name))
for name, x in data:
    m.append(stop(x, DY))
    m.append(label(x, DY + 26, name))
for i, (name, x) in enumerate(ops):
    m.append(stop(x, DY))
    m.append(label(x, DY + 26 if i % 2 == 0 else DY - 16, name))
# legend
lx = 40
for code, (col, en, ja) in LINES.items():
    m.append(f'<rect x="{lx}" y="446" width="26" height="18" rx="4" fill="{col}"/>')
    m.append(f'<text x="{lx+13}" y="459" text-anchor="middle" class="b">{code}</text>')
    m.append(f'<text x="{lx+34}" y="455" class="lg">{en}</text>')
    m.append(f'<text x="{lx+34}" y="469" class="lgj">{ja}</text>')
    lx += 155
save("stack.svg", "\n".join(m), 830, 484)


# 5. LED arrivals board for Medium articles (bilingual)
articles = [
    (("OCT 15", "10月15日"), ("Infra", "インフラ"), "#ffd166",
     ("We Were About to Pay ¥50,000 More a Month for a Bigger Disk.", "大きいディスクに月5万円多く払うところだった。")),
    (("SEP 25", "9月25日"), ("Infra", "インフラ"), "#ffd166",
     ("Object Storage for VPS Developers", "VPS開発者のためのオブジェクトストレージ")),
    (("SEP 15", "9月15日"), ("Net", "通信"), "#79c0ff",
     ("How to make your own Protocol (like HTTP) in 10 minutes", "10分で作る、HTTPのような自作プロトコル")),
    (("SEP 10", "9月10日"), ("Web", "ウェブ"), "#2bb3a3",
     ("All About HTTP Headers", "HTTPヘッダーのすべて")),
    (("JUL 06", "7月6日"), ("Essay", "随筆"), "#ff7b72",
     ("AI is making me faster, but I feel empty afterwards.", "AIで速くなった。でも、あとに残るのは虚しさ。")),
]
a = [f"""<defs>{DOTS}</defs>
<style>
.led{{font:700 15px {MONO_JP};fill:{AMBER}}}
.h{{font:700 12px {MONO_JP};fill:{DIM};letter-spacing:2px}}
.title{{font:800 20px {MONO};fill:{AMBER};letter-spacing:5px}}
.titlejp{{font:700 16px {JP};fill:{AMBER}}}
.new{{font:700 12px {MONO_JP};fill:#3ddc84}}
{SWAP}
</style>
<rect x="4" y="4" width="822" height="282" rx="14" fill="#16181b" stroke="#30363d" stroke-width="2"/>
<rect x="22" y="22" width="786" height="250" rx="6" fill="#050505"/>
<text x="40" y="56" class="title">ARRIVALS</text>
<text x="180" y="55" class="titlejp">到着案内</text>
{bi(790, 55, "h", "FROM: medium.com/@abhay.tiwari.er", "発: medium.com/@abhay.tiwari.er", R)}
{bi(40, 88, "h", "DATE", "日付")}{bi(122, 88, "h", "LINE", "路線")}{bi(210, 88, "h", "ARTICLE", "記事")}
<line x1="34" y1="98" x2="796" y2="98" stroke="#2a2a2a"/>"""]
for i, (d, line, col, title) in enumerate(articles):
    y = 126 + i * 32
    a.append(bi(40, y, "led", *d))
    a.append(bi(122, y, "led", *line, f' style="fill:{col}"'))
    a.append(bi(210, y, "led", *title))
    if i == 0:
        a.append(f'<g class="blink">{bi(790, y, "new", "NEW", "新着", R)}</g>')
    a.append(f'<line x1="34" y1="{y+11}" x2="796" y2="{y+11}" stroke="#1a1a1a"/>')
a.append('<rect x="22" y="22" width="786" height="250" rx="6" fill="url(#dots)" opacity=".45"/>')
save("articles.svg", "\n".join(a), 830, 290)
print("ok")
