import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
import os

URL = "http://www.shigahochi.co.jp/index.php"
resp = requests.get(URL)
soup = BeautifulSoup(resp.content, "html.parser")

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "滋賀報知新聞 新着記事"
ET.SubElement(channel, "link").text = URL
ET.SubElement(channel, "description").text = "毎朝自動生成されるフィード"

for dd in soup.select("dd.text2"):
    dt_elem = dd.find_previous_sibling("dt")
    a = dt_elem.find("a")
    title = a.get_text(strip=True)
    href = a["href"]
    link = href if href.startswith("http") else "http://www.shigahochi.co.jp/" + href
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    date_text = dd.get_text().split("｜")[0].strip()  # 例: "7月5日"
    dt = datetime.strptime(f"{datetime.now().year}年{date_text}", "%Y年%m月%d日")
    ET.SubElement(item, "pubDate").text = dt.strftime("%a, %d %b %Y 00:00:00 +0900")

tree = ET.ElementTree(rss)
cwd = os.getcwd()
print("CWD:", cwd)
output_path = os.path.join(cwd, "rss.xml")
tree.write(output_path, encoding="utf-8", xml_declaration=True)
print("Generated:", output_path, "size=", os.path.getsize(output_path))
