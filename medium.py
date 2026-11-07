"""Redraw the ARRIVALS board (assets/articles.svg) and the README article list from the Medium RSS feed.

Japanese titles and line tags come from articles.json, keyed by the Medium post id
(the hex at the end of the URL). A new post without an entry shows its English title
in both languages until a translation is added there.
"""
import datetime as dt, email.utils, json, re, urllib.request, xml.etree.ElementTree as ET

FEED = "https://medium.com/feed/@abhay.tiwari.er"
PROFILE = "https://medium.com/@abhay.tiwari.er"
SHOW = 5

MONO = "ui-monospace,SFMono-Regular,Consolas,Menlo,'Liberation Mono',monospace"
MONO_JP = MONO + ",'Yu Gothic','Meiryo','Hiragino Sans','Noto Sans JP'"
JP = "'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic UI','Yu Gothic','Meiryo','Noto Sans JP',sans-serif"
AMBER, DIM = "#ffb000", "#a8740a"
# Line tag guessed from Medium categories when articles.json has no entry: (category words, EN, JA, colour)
GUESS = [
    ({"go", "golang", "concurrency"}, "Go", "Go", "#79c0ff"),
    ({"networking", "protocol", "https", "http"}, "Net", "通信", "#79c0ff"),
    ({"devops", "linux", "aws-s3", "s3", "object-storage", "mysql", "database"}, "Infra", "インフラ", "#ffd166"),
    ({"security", "malware", "hacking"}, "Sec", "防御", "#ff7b72"),
    ({"ai", "llm", "cognition"}, "Essay", "随筆", "#ff7b72"),
    ({"web-development", "javascript", "laravel", "php", "software-engineering"}, "Web", "ウェブ", "#2bb3a3"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cut(s, n):
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def fetch():
    req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (profile-readme-bot)"})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
    posts = []
    for item in root.find("channel").findall("item"):
        url = item.findtext("link").split("?")[0]
        posts.append({
            "id": url.rsplit("-", 1)[-1],
            "url": url,
            "title": item.findtext("title").strip(),
            "date": email.utils.parsedate_to_datetime(item.findtext("pubDate")).date(),
            "cats": {c.text for c in item.findall("category")},
        })
    return posts[:SHOW]


def board(posts, extra):
    def bi(x, y, cls, en, ja, attrs=""):
        return (f'<text x="{x}" y="{y}" class="{cls} en"{attrs}>{esc(en)}</text>'
                f'<text x="{x}" y="{y}" class="{cls} ja"{attrs}>{esc(ja)}</text>')

    R = ' text-anchor="end"'
    a = [f"""<defs><pattern id="dots" width="3" height="3" patternUnits="userSpaceOnUse">
<rect x="2" width="1" height="3" fill="#000"/><rect y="2" width="3" height="1" fill="#000"/>
</pattern></defs>
<style>
.led{{font:700 15px {MONO_JP};fill:{AMBER}}}
.h{{font:700 12px {MONO_JP};fill:{DIM};letter-spacing:2px}}
.title{{font:800 20px {MONO};fill:{AMBER};letter-spacing:5px}}
.titlejp{{font:700 16px {JP};fill:{AMBER}}}
.new{{font:700 12px {MONO_JP};fill:#3ddc84}}
.en{{animation:en 8s infinite}}.ja{{animation:ja 8s infinite}}
@keyframes en{{0%,44%{{opacity:1}}50%,94%{{opacity:0}}100%{{opacity:1}}}}
@keyframes ja{{0%,44%{{opacity:0}}50%,94%{{opacity:1}}100%{{opacity:0}}}}
.blink{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
</style>
<rect x="4" y="4" width="822" height="282" rx="14" fill="#16181b" stroke="#30363d" stroke-width="2"/>
<rect x="22" y="22" width="786" height="250" rx="6" fill="#050505"/>
<text x="40" y="56" class="title">ARRIVALS</text>
<text x="180" y="55" class="titlejp">到着案内</text>
{bi(790, 55, "h", "FROM: medium.com/@abhay.tiwari.er", "発: medium.com/@abhay.tiwari.er", R)}
{bi(40, 88, "h", "DATE", "日付")}{bi(122, 88, "h", "LINE", "路線")}{bi(210, 88, "h", "ARTICLE", "記事")}
<line x1="34" y1="98" x2="796" y2="98" stroke="#2a2a2a"/>"""]
    newest = max(p["date"] for p in posts)
    for i, p in enumerate(posts):
        y = 126 + i * 32
        x = extra.get(p["id"], {})
        tag = x.get("tag") or next(((en, ja, col) for words, en, ja, col in GUESS if words & p["cats"]), ("Blog", "ブログ", AMBER))
        d = p["date"]
        is_new = d == newest and (dt.date.today() - d).days <= 30
        width = 63 if is_new else 68  # chars; ~8.3px each at 15px mono, NEW badge needs ~40px
        a.append(bi(40, y, "led", d.strftime("%b %d").upper(), f"{d.month}月{d.day}日"))
        a.append(bi(122, y, "led", tag[0], tag[1], f' style="fill:{tag[2]}"'))
        a.append(bi(210, y, "led", cut(x.get("title", p["title"]), width), cut(x.get("ja", p["title"]), 30 if x.get("ja") else width)))
        if is_new:
            a.append(f'<g class="blink">{bi(790, y, "new", "NEW", "新着", R)}</g>')
        a.append(f'<line x1="34" y1="{y+11}" x2="796" y2="{y+11}" stroke="#1a1a1a"/>')
    a.append('<rect x="22" y="22" width="786" height="250" rx="6" fill="url(#dots)" opacity=".45"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 290" width="830" height="290">\n' + "\n".join(a) + "\n</svg>\n"


def readme_list(posts):
    lines = [f"- [{p['title']}]({p['url']})" for p in posts]
    lines.append(f"- [More on Medium]({PROFILE})")
    return "\n".join(lines)


if __name__ == "__main__":
    posts = fetch()
    extra = json.load(open("articles.json", encoding="utf-8"))
    open("assets/articles.svg", "w", encoding="utf-8", newline="\n").write(board(posts, extra))
    readme = open("Readme.md", encoding="utf-8").read()
    new = re.sub(r"(<!-- articles:start -->\n).*?(\n<!-- articles:end -->)",
                 lambda m: m.group(1) + readme_list(posts) + m.group(2), readme, flags=re.S)
    assert "<!-- articles:start -->" in new, "article markers missing from Readme.md"
    open("Readme.md", "w", encoding="utf-8", newline="\n").write(new)
    print("ok", [p["id"] for p in posts])
