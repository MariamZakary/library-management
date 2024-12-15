from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)

BOOKS_FILE = 'books.json'
try:
    with open(BOOKS_FILE, 'r') as file:
        books = json.load(file)
except FileNotFoundError:
    books = []

def save_books():
    try:
        with open(BOOKS_FILE, 'w') as file:
            json.dump(books, file)
    except IOError as e:
        print(f"Error saving books to file: {e}")

@app.route('/books', methods=['POST'])
def add_book():
    book = request.json
    books.append(book)
    save_books()
    return jsonify({"message": "Book added successfully", "book": book}), 200

@app.route('/books/search', methods=['GET'])
def search_books():
    try:
        title = request.args.get('title')
        author = request.args.get('author')
        genre = request.args.get('genre')
        published_year = request.args.get('published_year', type=int)

        filtered_books = [
            book for book in books
            if (not title or (book.get('title') and title.lower() in book['title'].lower())) and
               (not author or (book.get('author') and author.lower() in book['author'].lower())) and
               (not genre or (book.get('genre') and genre.lower() in book['genre'].lower())) and
               (not published_year or book.get('published_year') == published_year)
        ]
        return jsonify({"message": "Search results", "books": filtered_books}), 200
    except Exception as e:
        return jsonify({"error": "Failed to perform search", "details": str(e)}), 400

@app.route('/books', methods=['GET'])
def list_all_books():
    try:
        return jsonify({"message": "List of all books", "books": books}), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve books", "details": str(e)}), 400

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    updated_data = request.json
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_data)
            save_books()
            return jsonify({"message": "Book updated successfully", "book": book}), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book_route(isbn):
    return delete_book(isbn)

def delete_book(isbn):
    global books
    book_exists = any(book['isbn'] == isbn for book in books)
    if not book_exists:
        return jsonify({"error": "Book not found"}), 404
    books = [book for book in books if book['isbn'] != isbn]
    save_books()
    return jsonify({"message": "Book deleted successfully"}), 200

SWAGGER_URL = "/docs"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Books API'}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=6000)
