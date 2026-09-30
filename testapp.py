"""Offline API tests using Flask's test client (Open Library is mocked)."""
from unittest.mock import patch

import app as backend

client = backend.app.test_client()


def test_health():
    assert client.get("/api/health").get_json() == {"status": "ok"}


def test_search_requires_query():
    assert client.get("/api/search").status_code == 400


def test_search_returns_short_ids():
    fake = [{"title": "Book A", "authors": ["X"], "work_id": "/works/OL1W"}]
    with patch.object(backend, "find_book_options", return_value=fake):
        data = client.get("/api/search?q=book").get_json()
    assert data["results"] == [{"id": "OL1W", "title": "Book A", "authors": ["X"], "cover": None}]


def test_recommendations_ok_and_passes_book_info():
    fake = [{"title": "B", "author": ["Y"], "score": 0.5, "shared": ["magic"]}]
    with patch.object(backend, "recommend_books", return_value=fake) as m:
        r = client.get("/api/books/OL1W/recommendations?title=A&author=X&n=3")
    assert r.status_code == 200
    book = m.call_args.args[0]
    assert book == {"work_id": "/works/OL1W", "title": "A", "authors": ["X"]}
    assert m.call_args.kwargs["n"] == 3


def test_recommendations_not_found_and_bad_id():
    with patch.object(backend, "recommend_books", return_value=[]):
        assert client.get("/api/books/OL1W/recommendations").status_code == 404
    assert client.get("/api/books/bad/recommendations").status_code == 400


def test_frontend_is_served():
    r = client.get("/")
    assert r.status_code == 200 and b"<title>" in r.data
    r.close()