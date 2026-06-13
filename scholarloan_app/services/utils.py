from datetime import datetime
import re
import dateparser

def parse_date(value: str):
    if not value:
        return None
    return dateparser.parse(value, settings={"PREFER_DATES_FROM": "past"})

def clean_amount(text: str):
    if not text: return None
    m = re.search(r'(\$|₹|€|£)\s?[\d,]+(?:\.\d+)?', text)
    return m.group(0) if m else None

def normalize_record(rec: dict):
    return {
        "title": (rec.get("title") or "").strip(),
        "link": (rec.get("link") or "").strip(),
        "provider": (rec.get("provider") or "").strip(),
        "amount": rec.get("amount"),
        "deadline": (rec.get("deadline") or "").strip(),
        "snippet": (rec.get("snippet") or "").strip(),
        "posted_at": rec.get("posted_at"),  # datetime or None
    }

def normalize_and_sort(items: list):
    norm = [normalize_record(x) for x in items if x.get("title") and x.get("link")]
    # latest first; missing dates go last
    norm.sort(key=lambda x: x["posted_at"] or datetime(1970,1,1), reverse=True)
    return norm

def make_keywords(criteria: dict):
    """Keywords from form: stream + country + category."""
    kws = []
    stream = (criteria.get("stream") or "").lower()
    if stream:
        kws += re.split(r'[\s/&,-]+', stream)

    c = (criteria.get("country") or "").lower()
    if c: kws.append(c)

    cat = (criteria.get("category") or "")
    cat_map = {
        "sc_st": ["sc", "st", "scheduled caste", "scheduled tribe"],
        "obc": ["obc", "other backward"],
        "minority": ["minority", "minorities"],
    }
    kws += cat_map.get(cat, [])
    return [k for k in kws if k and len(k) >= 3]
