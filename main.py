from book_api import find_book_options
from recommender import recommend_books


def main():
    options = find_book_options(input("Enter a book name: "))[:10]
    if not options:
        print("Book not found.")
        return

    for i, b in enumerate(options, 1):
        print(f"{i}. {b['title']} — {', '.join(b['authors'])}")

    try:
        book = options[int(input("\nChoose a book number: ")) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    results = recommend_books(book)
    print("\nRECOMMENDATIONS\n" + "-" * 16)
    if not results:
        print("No recommendations found.")
    for r in results:
        print(f"{r['title']} — {', '.join(r['author'])} → {r['score']:.2f}")
        print(f"   shared: {', '.join(r['shared'][:5])}")


if __name__ == "__main__":
    main()