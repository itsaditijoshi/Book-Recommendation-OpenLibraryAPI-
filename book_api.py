"""Thin, cached wrapper around the Open Library API."""
from functools import lru_cache

import requests

BASE_URL = "https://openlibrary.org"
TIMEOUT = 10
SEARCH_FIELDS = "key,title,author_name,subject,first_publish_year"

_session = requests.Session()
_session.headers["User-Agent"] = "book-recommender/1.0 (learning project)"

# Subjects that say nothing about what a book is *about*.
GENERIC_SUBJECTS = {
    "fiction", "juvenile fiction", "english language", "english fiction",
    "accessible book", "protected daisy", "in library", "lending library",
    "large type books", "open_syllabus_project", "reading level-grade 5",
    "long now manual for civilization",
}


def _get_json(url, params=None):
    try:
        response = _session.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return {}


def normalize_subjects(subjects):
    """Lowercase, dedupe and drop noise. Keeps the full vocabulary."""
    cleaned = set()
    for subject in subjects or []:
        if not isinstance(subject, str):
            continue
        s = subject.lower().strip()
        if (
            not s
            or len(s) > 40
            or s in GENERIC_SUBJECTS
            or ":" in s                      # nyt:..., series:..., place:...
            or "(fictitious" in s            # character names -> same-series bias
            or "series" in s
        ):
            continue
        cleaned.add(s)
    return cleaned


def search_books(query=None, subject=None, limit=10):
    """Search by free text and/or exact subject. Docs include subjects."""
    parts = []
    if query:
        parts.append(query)
    if subject:
        parts.append(f'subject:"{subject}"')
    if not parts:
        return []
    params = {"q": " ".join(parts), "limit": limit, "fields": SEARCH_FIELDS}
    return _get_json(f"{BASE_URL}/search.json", params).get("docs", [])


@lru_cache(maxsize=256)
def get_work_subjects(work_id):
    """Subjects for one work, normalized. Returns a frozenset (cacheable)."""
    data = _get_json(f"{BASE_URL}{work_id}.json")
    return frozenset(normalize_subjects(data.get("subjects")))


def find_book_options(query, limit=20):
    """Search results reduced to title / authors / work_id, deduped."""
    options, seen = [], set()
    for book in search_books(query=query, limit=limit):
        title, work_id = book.get("title"), book.get("key")
        if not title or not work_id:
            continue
        authors = book.get("author_name", [])
        ident = (title.lower(), tuple(authors))
        if ident in seen:
            continue
        seen.add(ident)
        options.append({"title": title, "authors": authors, "work_id": work_id})
    return options