"""Flask backend for the book recommender.

Run:  python app.py        (dev server on http://127.0.0.1:5000)
"""
from flask import Flask, jsonify, request

from book_api import find_book_options
from recommender import recommend_books

app = Flask(__name__, static_folder="static", static_url_path="")


@app.after_request
def add_cors(response):
    # Open during development; restrict to your frontend's origin in production.
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def _short_id(work_id):
    return work_id.rsplit("/", 1)[-1]          # "/works/OL82563W" -> "OL82563W"


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.get("/api/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify(error="Missing query parameter 'q'"), 400

    options = find_book_options(query)[:10]
    return jsonify(results=[
        {"id": _short_id(o["work_id"]), "title": o["title"], "authors": o["authors"]}
        for o in options
    ])


@app.get("/api/books/<olid>/recommendations")
def recommendations(olid):
    """Optional query params: title, author (repeatable), n (1-20, default 5)."""
    if not olid.startswith("OL") or not olid.endswith("W"):
        return jsonify(error="Invalid work id"), 400

    try:
        n = max(1, min(int(request.args.get("n", 5)), 20))
    except ValueError:
        return jsonify(error="'n' must be an integer"), 400

    book = {
        "work_id": f"/works/{olid}",
        "title": request.args.get("title", ""),
        "authors": request.args.getlist("author"),
    }
    results = recommend_books(book, n=n)
    if not results:
        return jsonify(error="No recommendations found for this book"), 404
    return jsonify(id=olid, recommendations=results)


if __name__ == "__main__":
    app.run(debug=True)