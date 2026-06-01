from bs4 import BeautifulSoup
import pandas as pd

def extract_tables(html_tables):
    tables_data = []

    for table_html in html_tables:
        soup = BeautifulSoup(table_html, "lxml")
        rows = []

        for tr in soup.find_all("tr"):
            cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append(cols)

        if rows:
            df = pd.DataFrame(rows)
            tables_data.append(df.to_string())

    return tables_data