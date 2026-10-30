import csv
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# 武蔵野大学トップページ
START_URL = "https://www.musashino-u.ac.jp/"
DOMAIN = urlparse(START_URL).netloc

# 辞書型変数（key: URL, value: <title>文字列）[cite: 2]
sitemap = {}
visited = set()
to_visit = [START_URL]

print("スクレイピングを開始します...")

while to_visit:
    url = to_visit.pop(0)

    if url in visited:
        continue

    visited.add(url)

    # 授業指定：アクセス時は必ず time.sleep(秒数) で負荷軽減[cite: 2, 22]
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

        # <title>タグ内の文字列を取得[cite: 2]
        title_text = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else ""
        )
        sitemap[url] = title_text
        print(f"取得: {url} -> {title_text}")

        # find_all ですべてのaタグを巡回[cite: 2, 17]
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag["href"])
            parsed = urlparse(link)

            # ページ内リンク（#）などを除去して正規化[cite: 2]
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

            # 同一ドメインかつ未訪問リンクのみキューに追加[cite: 2]
            if (
                parsed.netloc == DOMAIN
                and clean_url not in visited
                and clean_url not in to_visit
            ):
                to_visit.append(clean_url)

    except Exception as e:
        print(f"エラー ({url}): {e}")

# 辞書型変数を元にCSV保存[cite: 2]
with open("sitemap.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title"])
    for url, title in sitemap.items():
        writer.writerow([url, title])

print("\n完了しました。sitemap.csv に保存しました。")