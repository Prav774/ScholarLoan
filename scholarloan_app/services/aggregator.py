from .sources.generic_rss import fetch_generic_rss
from .utils import normalize_and_sort

def search_scholarships(criteria: dict, limit: int = 40):
    results = []
    try:
        results += fetch_generic_rss(criteria, max_items=limit * 2)
    except Exception as e:
        print(f"[aggregator] ERROR: {e}")

    results = normalize_and_sort(results)

    seen, dedup = set(), []
    for r in results:
        k = (r.get("link") or "").strip().lower()
        if k and k not in seen:
            seen.add(k)
            dedup.append(r)
        if len(dedup) >= limit:
            break
    return dedup
