import psycopg2
import requests
from bs4 import BeautifulSoup
import os
import random
import time
from tqdm import tqdm
from dotenv import load_dotenv

# 🔹 Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# --- DATABASE CONFIG ---
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# --- CONNECT TO DATABASE ---
print("🔗 Connecting to PostgreSQL...")
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()

# --- FETCH DATA WHERE DISCOVERY FACILITY CONTAINS "TESS" ---
print("🔍 Fetching exoplanet reference data...")
cursor.execute("""
    SELECT pl_refname 
    FROM exoplanets
    WHERE disc_facility ILIKE '%Transiting Exoplanet Survey Satellite (TESS)%'
    AND default_flag = true
""")
rows = cursor.fetchall()

# Close DB connection
cursor.close()
conn.close()

# --- FUNCTION TO EXTRACT URL FROM pl_refname HTML ---
def extract_link(html):
    """Extracts the hyperlink (href) from an <a> tag inside pl_refname."""
    soup = BeautifulSoup(html, "html.parser")
    link_tag = soup.find("a")
    if link_tag and link_tag.has_attr("href"):
        return link_tag["href"]
    return None  # No valid link found

def get_arxiv_id(text):
    """Removes the arXiv header from the reference text."""
    if text.startswith("arXiv:"):
        return text[6:].strip()
    return text

def create_pdf_link(arxiv_id):
    """Creates a direct link to the PDF version of an arXiv paper."""
    return f"https://arxiv.org/pdf/{arxiv_id}"

# --- FUNCTION TO SCRAPE arXiv REFERENCE ---
def get_arxiv_reference(url):
    """Scrapes the arXiv reference from the given link with rate limiting and improved parsing."""
    try:
        # Losowe opóźnienie 1-3 sekundy, aby uniknąć HTTP 429
        time.sleep(random.uniform(1, 3))  
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # --- 1. Wyszukiwanie wprost w <a> z data-target="arXiv"
        arxiv_link = soup.find("a", {"data-target": "arXiv"})
        if arxiv_link and arxiv_link.text:
            arxiv_id = get_arxiv_id(arxiv_link.text.strip())
            return create_pdf_link(arxiv_id)

        # --- 2. Alternatywa: Szukanie <dt> z "arXiv" i pobranie wartości z <dd>
        dt_tags = soup.find_all("dt")
        for dt in dt_tags:
            if "arXiv" in dt.text:
                arxiv_dd = dt.find_next_sibling("dd")
                if arxiv_dd:
                    arxiv_a = arxiv_dd.find("a")
                    if arxiv_a and arxiv_a.text:
                        arxiv_id = get_arxiv_id(arxiv_a.text.strip())
                        return create_pdf_link(arxiv_id)

        return "❌ No arXiv reference found"

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print(f"⚠️ Rate limit reached! Waiting before retrying...")
            time.sleep(random.uniform(10, 20))  # Dłuższe oczekiwanie
            return get_arxiv_reference(url)  # Ponowna próba

        return f"❌ Error fetching {url}: {e}"

    except requests.RequestException as e:
        return f"❌ Error fetching {url}: {e}"

# --- PROCESS LINKS ---
print("🔗 Extracting reference links...")
arxiv_references = {}

for row in tqdm(rows[397:], desc="Processing references"):
    raw_html = row[0]  # The pl_refname column contains HTML
    link = extract_link(raw_html)
    print(link)

    if link and link.startswith("http"):  # Ensure it's a valid URL
        ref = get_arxiv_reference(link)
        arxiv_references[link] = ref

        # Append to file immediately
        with open("arxiv_references.txt", "a") as f:
            f.write(f"{ref}\n")


# --- PRINT RESULTS ---
# print("\n✅ Extracted arXiv References:")
# for link, ref in arxiv_references.items():
#     print(f"{link} → {ref}")

# Optionally, save results to a file
# with open("arxiv_references.txt", "w") as f:
#     for link, ref in arxiv_references.items():
#         f.write(f"{ref}\n")

# print("\n📁 Saved results to arxiv_references.txt")

# --- TEST FUNCTIONS ---
# test = get_arxiv_reference("https://ui.adsabs.harvard.edu/abs/2022AJ....163..223H/abstract")
# cleaned = get_arxiv_id(test)
# link = create_pdf_link(cleaned)
# print(test)