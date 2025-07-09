import requests, datetime, email.utils, pathlib, html
from bs4 import BeautifulSoup

BASE_URL = "http://www.shigahochi.co.jp/"
TOP_URL = BASE_URL
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
last_build = email.utils.format_datetime(now)

# 取得
r = requests.get(TOP_URL, timeout=20)
r.encoding = 'shift_jis'
soup = BeautifulSoup(r.text, "html.parser")  # ← lxml → html.parser に変更！

# 記事リンクを抽出
items = []
for a in soup.select("p.sp-caption-txt1 a"):
    title = a.get_text(strip=True)
    link = a["href"]
    if not link.startswith("http"):
        link = BASE_URL + link.lstrip("./")
    pub = email.utils.format_datetime(now)
    items.append(
        f"<item><title>{html.escape(title)}</title><link>{link}</link><guid>{link}</guid><pubDate>{pub}</pubDate></item>"
    )

if not items:
    print("WARNING: RSSアイテムが見つかりません。rss.xmlを生成しません。")
    exit(0)

rss = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<rss version="2.0">\n<channel>\n'
    '<title>滋賀報知新聞 新着記事</title>\n'
    f'<link>{TOP_URL}</link>\n'
    '<description>滋賀報知新聞トップページの新着記事をRSS配信</description>\n'
    f'<lastBuildDate>{last_build}</lastBuildDate>\n'
    + "\n".join(items) +
    '\n</channel>\n</rss>'
)

pathlib.Path("rss.xml").write_text(rss, encoding="utf-8")
print("[DEBUG] rss.xml written")
