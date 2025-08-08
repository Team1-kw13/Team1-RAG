import requests
from bs4 import BeautifulSoup
import json

url = "https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=13100000015"
headers = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(url, headers=headers)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

div_left = soup.select_one("div.left")
docs = []
current_title = None

for node in div_left.find_all(['h3','p','li','div'], recursive=True):
    if node.name == 'h3' and 'tit_dep_2' in node.get('class', []):
        current_title = node.get_text(strip=True)
    elif current_title:
        text = node.get_text(" ", strip=True)
        if text:
            docs.append({
                "title": current_title,
                "content": text,
                "source": url
            })

# JSON 파일로 저장
with open("rag_docs.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)
