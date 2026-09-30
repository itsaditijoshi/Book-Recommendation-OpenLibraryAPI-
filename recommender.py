"""Subject-overlap book recommender."""
from book_api import get_work_subjects, normalize_subjects, search_books


def jaccard_similarity(a, b):
    a, b = set(a), set(b)
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def _same_book_or_author(candidate, book):
    if candidate.get("key") == book["work_id"]:
        return True
    if (candidate.get("title") or "").lower() == book["title"].lower():
        return True
    return bool(set(candidate.get("author_name", [])) & set(book["authors"]))


def recommend_books(book, n=5, top_subjects=4, per_subject=25):
    """book: dict with title, authors, work_id (from find_book_options)."""
    selected = get_work_subjects(book["work_id"])
    if not selected:
        return []

    # 1. Candidate pool: exact-subject searches (docs already carry subjects,
    #    so no per-candidate API call is needed).
    pool = {}
    for subject in sorted(selected)[:top_subjects]:
        for doc in search_books(subject=subject, limit=per_subject):
            if doc.get("key") and doc.get("title") and not _same_book_or_author(doc, book):
                pool[doc["key"]] = doc

    # 2. Score, skipping duplicate titles and zero-overlap books.
    results, seen_titles = [], set()
    for doc in pool.values():
        title = doc["title"].lower()
        if title in seen_titles:
            continue
        subjects = normalize_subjects(doc.get("subject"))
        shared = selected & subjects
        if not shared:
            continue
        seen_titles.add(title)
        results.append({
            "title": doc["title"],
            "author": doc.get("author_name", []),
            "score": jaccard_similarity(selected, subjects),
            "shared": sorted(shared),
        })

    results.sort(key=lambda r: (r["score"], len(r["shared"])), reverse=True)
    return results[:n]