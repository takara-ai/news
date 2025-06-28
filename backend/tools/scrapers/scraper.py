from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

from .llm_scraper import extract

http = urllib3.PoolManager()
def extract_main_content(html_content: str, base_url: str = None) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')

    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            src = urljoin(base_url, src) if base_url else src
            images.append({
                "alt": img.get('alt') or None,
                "image_url": src
            })

    # Remove common non-content tags
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return {
        "text": text,
        "images": images
    }

def scrape(url: str) -> dict:
    response = http.request('GET', url)

    html_content = response.data.decode('utf-8')
    base_url = urljoin(url, '/')

    main_content = extract_main_content(html_content, base_url)
    main_content['text'] = extract(main_content['text'])

    return {
        "text": main_content['text'],
        "images": main_content['images']
    }