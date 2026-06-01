from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json


visited = set()
data = []


def crawl(url, driver):
    if url in visited:
        return

    visited.add(url)

    try:
        driver.get(url)
        time.sleep(2)

        # Extract text
        text = driver.find_element(By.TAG_NAME, "body").text

        # Extract links
        links = driver.find_elements(By.TAG_NAME, "a")
        links = [l.get_attribute("href") for l in links if l.get_attribute("href")]

        # Extract images
        images = driver.find_elements(By.TAG_NAME, "img")
        images = [img.get_attribute("src") for img in images]

        # Extract PDFs
        pdfs = [l for l in links if ".pdf" in l]

        data.append({
            "url": url,
            "text": text,
            "images": images,
            "pdfs": pdfs
        })

        # Recursive crawl
        for link in links:
            if "iiitu.ac.in" in link:
                crawl(link, driver)

    except Exception as e:
        print("Error:", e)


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    crawl("https://iiitu.ac.in/", driver)

    with open("../data/raw/output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    driver.quit()


if __name__ == "__main__":
    main()