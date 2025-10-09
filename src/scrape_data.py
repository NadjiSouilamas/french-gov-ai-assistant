import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

DATA_DIR = os.path.join("..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)


URLS = [
    "https://www.service-public.fr/particuliers/vosdroits/F1361", 
    "https://www.service-public.fr/particuliers/vosdroits/F2828", 
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F16511", 
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F16548",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2890",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2832",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F31083",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2830",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2826",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F10036",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F21012",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2825",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2833",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2845",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F11629",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2843",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2846",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F31121",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F31124",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2844",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F2848",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F31128",
    "https://www.service-public.gouv.fr/particuliers/vosdroits/F31129"
    "https://www.service-public.fr/particuliers/vosdroits/F12006",
    "https://www.service-public.fr/particuliers/vosdroits/F931",  
]





def clean_text(text: str) -> str:
    """Simple cleanup for extra whitespace."""
    text = text.replace("\n", " ").replace("\r", "")
    text = " ".join(text.split())
    return text

def scrape_page(url: str) -> str:
    """Download and extract main content from a Service-Public.fr page."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract main content
    main_content = soup.find("main")
    if not main_content:
        main_content = soup  # fallback

    paragraphs = [p.get_text() for p in main_content.find_all(["p", "li"])]
    content = clean_text(" ".join(paragraphs))
    return content

def save_text(content: str, url: str):
    """Save page content as a .txt file."""
    page_id = os.path.basename(urlparse(url).path)
    filename = os.path.join(RAW_DIR, f"{page_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Saved {filename} ({len(content)} chars)")

def main():
    for url in URLS:
        try:
            content = scrape_page(url)
            save_text(content, url)
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")

if __name__ == "__main__":
    main()
