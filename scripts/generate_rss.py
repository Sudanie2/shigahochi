--- scripts/generate_rss.py
+++ scripts/generate_rss.py
@@
- for dd in soup.select("dd.text2"):
-    # 修正：find_previous で <dt> を取得
-    dt_elem = dd.find_previous("dt")
-    a = dt_elem.find("a")
-    title = a.get_text(strip=True)
-    href = a["href"]
-    link = href if href.startswith("http") else "http://www.shigahochi.co.jp/" + href
-
-    item = ET.SubElement(channel, "item")
-    ET.SubElement(item, "title").text = title
-    ET.SubElement(item, "link").text = link
-
-    date_text = dd.get_text().split("｜")[0].strip()  # 例: "7月5日"
-    dt = datetime.strptime(f"{datetime.now().year}年{date_text}", "%Y年%m月%d日")
-    ET.SubElement(item, "pubDate").text = dt.strftime("%a, %d %b %Y 00:00:00 +0900")
+ # 「トップニュース」スライダーから取得
+ for slide in soup.select("div.sp-slide"):
+     a = slide.select_one(".sp-caption-txt1 a")
+     title = a.get_text(strip=True)
+     href  = a["href"]
+     link  = href if href.startswith("http") else "http://www.shigahochi.co.jp/" + href
+
+     date_txt = slide.select_one(".sp-caption-txt3").get_text()  # 例: "(東近江・湖東 ニュース 7月5日)"
+     # 最後の「月日」を抜き出す
+     m = date_txt.strip("()").split()[-1]
+     dt = datetime.strptime(f"{datetime.now().year}年{m}", "%Y年%m月%d日")
+
+     item = ET.SubElement(channel, "item")
+     ET.SubElement(item, "title").text   = title
+     ET.SubElement(item, "link").text    = link
+     ET.SubElement(item, "pubDate").text = dt.strftime("%a, %d %b %Y 00:00:00 +0900")
