"""Offline tests: no network needed (API calls are mocked)."""
from unittest.mock import patch

import recommender
from recommender import jaccard_similarity, recommend_books

BOOK = {"title": "Book A", "authors": ["Author A"], "work_id": "/works/A"}
SUBJECTS = frozenset({"magic", "wizards", "school"})


def doc(key, title, author, subjects):
    return {"key": key, "title": title, "author_name": [author], "subject": subjects}


def test_jaccard():
    assert jaccard_similarity(["a", "b", "c"], ["a", "b", "d"]) == 0.5
    assert jaccard_similarity([], []) == 0.0


def test_recommendations_filtered_and_ranked():
    docs = [
        doc("/works/A", "Book A", "Author A", ["magic"]),           # itself
        doc("/works/B", "Book B", "Author A", ["magic", "school"]), # same author
        doc("/works/C", "Book C", "Author C", ["magic", "wizards", "school"]),
        doc("/works/D", "Book D", "Author D", ["magic"]),
        doc("/works/E", "Book E", "Author E", ["cooking"]),          # no overlap
        doc("/works/F", "book c", "Author F", ["magic"]),            # duplicate title
    ]
    with patch.object(recommender, "get_work_subjects", return_value=SUBJECTS), \
         patch.object(recommender, "search_books", return_value=docs):
        results = recommend_books(BOOK)

    assert [r["title"] for r in results] == ["Book C", "Book D"]
    assert results[0]["score"] == 1.0


def test_no_subjects_returns_empty():
    with patch.object(recommender, "get_work_subjects", return_value=frozenset()):
        assert recommend_books(BOOK) == []