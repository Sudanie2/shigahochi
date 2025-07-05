import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

URL = "http://www.shigahochi.co.jp/index.php"
resp = requests.get(URL)
soup = BeautifulSoup(resp.content, "html.parser")

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "滋賀報知新聞 新着記事"
ET.SubElement(channel, "link").text = URL
ET.SubElement(channel, "description").text = "毎朝自動生成されるフィード"

for dd in soup.select("dd.text2"):
    parent = dd.find_previous_sibling("dt")
    a = parent.find("a")
    title = a.get_text(strip=True)
    link = "http://www.shigahochi.co.jp/" + a["href"].replace("info.php?","")
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    date_str = dd.get_text().split("｜")[0].strip()
    dt = datetime.strptime(f"{datetime.now().year}年{date_str}", "%Y年%m月%d日")
    ET.SubElement(item, "pubDate").text = dt.strftime("%a, %d %b %Y 00:00:00 +0900")

tree = ET.ElementTree(rss)
tree.write("rss.xml", encoding="utf-8", xml_declaration=True)
