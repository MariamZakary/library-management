Library Management
A Flask-based RESTful API for managing a collection of books in a library.
Features:
Add new books
List all books
Search books by author, year, or genre
Update book details
Delete books
Endpoints
HTTP Method	Endpoint	Description
POST	/books	Add a new book
GET	/books	List all books
GET	/books/search	Search for books
PUT	/books/{isbn}	Update book details
DELETE	/books/{isbn}	Delete a book by ISBN
