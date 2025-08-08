from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os

SEARCH_QUERY = "등본"
PAGE_COUNT = 5  # 크롤링할 페이지 수
SAVE_PATH = f"docs/cleaned/gov_faq_{SEARCH_QUERY}.txt"
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

def setup_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def crawl_page(driver, page_no):
    url = f"https://plus.gov.kr/portal/faq?pageNo={page_no}&srchClsf=whol&srchCn={SEARCH_QUERY}&pageSz=10"
    driver.get(url)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    faq_list = soup.select("li.accordion-item")

    results = []
    for item in faq_list:
        q_elem = item.select_one("span.accordion-title")
        a_elem = item.select_one("div.accordion-contetns")

        if q_elem and a_elem:
            question = q_elem.get_text(strip=True)
            answer = a_elem.get_text(" ", strip=True)
            results.append((question, answer))
    return results

def save_to_txt(all_data):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        for i, (q, a) in enumerate(all_data, 1):
            f.write(f"[문서: FAQ #{i}]\nQ: {q}\nA: {a}\n\n")
    print(f"{len(all_data)}개 항목 저장 완료 → {SAVE_PATH}")

def main():
    driver = setup_driver()
    all_data = []

    try:
        for page in range(1, PAGE_COUNT + 1):
            print(f"[크롤링 중] page {page}")
            page_data = crawl_page(driver, page)
            if not page_data:
                print("더 이상 항목 없음")
                break
            all_data.extend(page_data)
            time.sleep(1)
    finally:
        driver.quit()

    save_to_txt(all_data)

if __name__ == "__main__":
    main()
