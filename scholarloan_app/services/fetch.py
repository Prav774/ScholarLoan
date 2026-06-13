import random, time, requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.conf import settings

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/124.0",
]

TIMEOUT = getattr(settings, "SCHOLAR_HTTP_TIMEOUT", 12)
RETRIES = getattr(settings, "SCHOLAR_HTTP_RETRIES", 2)
VERIFY = getattr(settings, "SCHOLAR_HTTP_VERIFY", True)

def fetch_text(url: str, cache_sec: int = 600, params=None):
    key = f"fetch:{url}:{params}"
    cached = cache.get(key)
    if cached:
        return cached

    headers = {"User-Agent": random.choice(UAS), "Accept-Language": "en-US,en;q=0.9"}
    last = None
    for i in range(RETRIES + 1):
        try:
            r = requests.get(url, headers=headers, params=params, timeout=TIMEOUT, verify=VERIFY)
            if r.status_code == 200:
                cache.set(key, r.text, cache_sec)
                return r.text
            print(f"[fetch_text] {url} -> HTTP {r.status_code}")
            time.sleep(0.6 + 0.4*i)
        except Exception as e:
            last = e
            print(f"[fetch_text] ERROR fetching {url}: {e}")
            time.sleep(0.8 + 0.5*i)
    if last:
        print(f"[fetch_text] giving up on {url}: {last}")
        return None
    return None

def soupify(text: str, parser="lxml-xml"):
    if not text:
        return None
    # be forgiving (XML -> HTML fallback)
    try:
        return BeautifulSoup(text, parser)
    except Exception as e:
        print(f"[soupify] XML parse failed, retrying with html.parser: {e}")
        try:
            return BeautifulSoup(text, "html.parser")
        except Exception as e2:
            print(f"[soupify] html.parser failed: {e2}")
            return None
