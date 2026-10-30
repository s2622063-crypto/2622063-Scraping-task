import csv
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

START_URL = "https://www.musashino-u.ac.jp/"
DOMAIN = urlparse(START_URL).netloc

visited = set()
to_visit = [START_URL]
csv_filename = "sitemap.csv"

# CSVファイルのヘッダー作成[cite: 2]
with open(csv_filename, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title"])

print("スクレイピングを開始します...")

while to_visit:
    url = to_visit.pop(0)

    if url in visited:
        continue

    visited.add(url)

    # 負荷軽減待機[cite: 2, 22]
    time.sleep(1)

    try:
        res = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            },
        )

        if "text/html" not in res.headers.get("Content-Type", ""):
            continue

        soup = BeautifulSoup(res.content, "html.parser")
        title_text = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else ""
        )

        # 1件取得するごとにその場でCSVに保存
        with open(csv_filename, "a", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([url, title_text])

        print(f"取得・保存完了: {url} -> {title_text}")

        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag["href"])
            parsed = urlparse(link)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

            if (
                parsed.netloc == DOMAIN
                and clean_url not in visited
                and clean_url not in to_visit
            ):
                to_visit.append(clean_url)

    except Exception as e:
        print(f"エラー ({url}): {e}")