from datetime import datetime
from ..fetch import fetch_text, soupify
from ..utils import parse_date, clean_amount, make_keywords

DEFAULT_FEEDS = [
    "https://scholarship-positions.com/feed/",
    "https://www.scholarships.com/Blog/rss",
]

def _collect(url, max_items):
    xml = fetch_text(url, cache_sec=300)
    soup = soupify(xml, parser="lxml-xml")
    out = []
    if not soup:
        print(f"[generic_rss] No soup for {url}")
        return out

    for item in soup.find_all(["item", "entry"]):
        title = (item.title.text if item.title else "").strip()

        link = ""
        link_tag = item.find("link")
        if link_tag:
            link = link_tag.get("href") or link_tag.text or ""

        desc = ""
        if item.find("description"): desc = item.description.text
        elif item.find("summary"): desc = item.summary.text
        desc = (desc or "").strip()

        pub = ""
        for tag in ("pubDate", "updated", "published"):
            t = item.find(tag)
            if t and t.text:
                pub = t.text
                break
        posted_at = parse_date(pub) or datetime.utcnow()

        out.append({
            "title": title,
            "link": link.strip(),
            "provider": "RSS",
            "amount": clean_amount(desc),
            "deadline": "",
            "snippet": (desc[:220] + "...") if len(desc) > 220 else desc,
            "posted_at": posted_at,
        })
        if len(out) >= max_items:
            break
    return out

def fetch_generic_rss(criteria: dict, max_items: int = 30, feeds=None):
    feeds = feeds or DEFAULT_FEEDS
    keywords = [k.lower() for k in make_keywords(criteria)]
    collected = []

    for url in feeds:
        try:
            collected += _collect(url, max_items=max_items)
        except Exception as e:
            print(f"[generic_rss] ERROR {url}: {e}")

    if not collected:
        return []  # network or parsing failed

    # try keyword filter
    if keywords:
        filtered = []
        for r in collected:
            hay = f"{r['title']} {r.get('snippet','')}".lower()
            if any(k in hay for k in keywords):
                filtered.append(r)
        if filtered:
            filtered.sort(key=lambda x: x["posted_at"], reverse=True)
            return filtered[:max_items]

    # fallback: latest anyway
    collected.sort(key=lambda x: x["posted_at"], reverse=True)
    return collected[:max_items]
