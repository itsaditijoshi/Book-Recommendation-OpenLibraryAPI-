# 📚 Book Recommendation System

A book recommendation system that uses the **Open Library API** to search for real books and generate book recommendations based on their available metadata.

The project uses **Flask** for the backend and is designed to provide book search and recommendation APIs that can be connected to a frontend.

---

## 🚀 Features

* 🔎 Search for books using a book name
* 📚 Uses real book data from the Open Library API
* 👤 Displays book titles and authors
* 🆔 Uses Open Library Work IDs to identify books
* 🤖 Generates recommendations using a similarity-based recommendation system
* 🌐 Flask REST API backend
* ❤️ Health-check endpoint to verify that the backend is running
* 🔄 JSON responses for easy frontend integration
* 🛡️ Basic validation for API requests

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Requests**
* **Open Library API**
* **Jaccard Similarity**
* **HTML / CSS / JavaScript** for the frontend

---

## 📂 Project Structure

```text
Book-Recommendation-OpenLibraryAPI/
│
├── app.py
├── book_api.py
├── recommender.py
│
├── test_api.py
├── test_recommender.py
├── test_recommender_api.py
│
├── static/
│   └── index.html
│
├── .gitignore
├── venvconfig
└── README.md
```

> The exact files may vary depending on the current version of the project.

---

## 🔄 How the Project Works

The overall flow is:

```text
User enters a book name
        ↓
Flask backend
        ↓
Open Library API
        ↓
Book search results
        ↓
User selects a book
        ↓
Open Library Work ID
        ↓
Recommendation system
        ↓
Similarity calculation
        ↓
Recommended books
        ↓
JSON response
        ↓
Frontend
```

---

## 🔎 1. Searching for a Book

The user enters a book name.

For example:

```text
The Alchemist
```

The Flask backend receives the request through:

```text
/api/search?q=The%20Alchemist
```

The backend calls the Open Library API and returns book options containing information such as:

* Book title
* Author
* Open Library Work ID

Example response:

```json
{
  "results": [
    {
      "id": "OL24793570W",
      "title": "The Alchemist",
      "authors": ["Paulo Coelho"]
    }
  ]
}
```

---

## 📖 2. Selecting a Book

A book is identified using its **Open Library Work ID**.

For example:

```text
OL24793570W
```

This prevents the recommendation system from relying only on the book title, since multiple books can have similar or identical titles.

---

## 🤖 3. Generating Recommendations

After a book is selected, the backend sends its Work ID to the recommendation system.

The recommendation system retrieves information about the selected book from Open Library and compares it with candidate books.

The similarity calculation is then used to rank the candidate books.

---

## 📊 4. Jaccard Similarity

The current recommendation prototype uses **Jaccard similarity** for comparing sets of book subjects/features.

The basic idea is:

```text
Similarity =
common features
----------------
all unique features
```

For example:

```text
Book A:
Fantasy, Magic, Adventure

Book B:
Fantasy, Magic, Mystery
```

Common:

```text
Fantasy, Magic
```

Total unique:

```text
Fantasy, Magic, Adventure, Mystery
```

Therefore:

```text
Similarity = 2 / 4 = 0.50
```

A higher value means the two books have more overlapping features.

---

## 🌐 Flask API

The Flask backend currently provides the following endpoints.

### Health Check

```text
GET /api/health
```

Used to check whether the backend is running.

Response:

```json
{
  "status": "ok"
}
```

---

### Search Books

```text
GET /api/search?q=Harry%20Potter
```

Returns book options from Open Library.

---

### Get Recommendations

```text
GET /api/books/<work_id>/recommendations
```

Example:

```text
/api/books/OL82563W/recommendations
```

The number of recommendations can also be specified:

```text
/api/books/OL82563W/recommendations?n=10
```

The API supports between **1 and 20 recommendations**, with 5 as the default.

---

## ▶️ Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/itsaditijoshi/Book-Recommendation-OpenLibraryAPI.git
```

Move into the project folder:

```bash
cd Book-Recommendation-OpenLibraryAPI
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```bash
pip install flask requests
```

---

### 4. Run the Flask application

```bash
python app.py
```

The development server will run at:

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing

The project contains test files for testing different parts of the system.

Examples include:

```text
test_api.py
test_recommender.py
test_recommender_api.py
```

These can be used to test API communication and recommendation logic independently before connecting everything to the frontend.

---

## 🌍 Data Source

This project uses the **Open Library API** to retrieve real book information.

The recommendations are therefore generated from book information retrieved through the API rather than from a manually created dummy book database.

---

## ⚠️ Current Limitations

Open Library contains a large amount of metadata, but the availability and quality of metadata can vary between books.

Some books may have:

* incomplete subjects
* different editions or language titles
* duplicate records
* limited metadata
* search results that do not perfectly match the user's query

Because of this, recommendation quality can vary depending on the selected book.

---

## 🔮 Future Improvements

Possible improvements include:

* Improve book matching and selection
* Use additional book metadata instead of relying heavily on subjects
* Improve the recommendation algorithm
* Add TF-IDF and cosine similarity
* Add author similarity
* Add description-based similarity
* Display book covers
* Display descriptions and publication information
* Improve frontend UI
* Add loading and error states
* Deploy the Flask backend
* Deploy the frontend
* Add more comprehensive automated tests

---

## 🎯 Project Goal

The goal of this project is to build a recommendation system that demonstrates how **real-world API data can be combined with a recommendation algorithm and a web backend** to provide personalized book recommendations.

---

## 👩‍💻 Author

**Aditi Joshi**

GitHub:
https://github.com/itsaditijoshi
