from django.test import TestCase
from unittest.mock import patch, MagicMock
from authors.models import Author
from books.models import Book, AuthorBook
from books.tasks import import_books
import pandas as pd


class ImportBooksTaskTestCase(TestCase):

    def setUp(self):
        # Set up authors to be referenced by books
        self.author1 = Author.objects.create(
            name="Author 1",
            external_id=1,
            about="An author of fiction."
        )
        self.author2 = Author.objects.create(
            name="Author 2",
            external_id=2,
            about="A well-known non-fiction author."
        )

    @patch('books.tasks.pd.read_json')  # Mock the pd.read_json function
    def test_import_books(self, mock_read_json):
        # Mock data for the chunks as if read from a JSON file
        mock_chunk_data = [
            {
                "title": "Book 1",
                "isbn": "1234567890",
                "isbn13": "1234567890123",
                "language": "English",
                "publisher": "Publisher 1",
                "publication_date": "2020-01-01",
                "format": "Hardcover",
                "series_name": "Series A",
                "series_position": "1",
                "image_url": "http://example.com/book1.jpg",
                "description": "A great book about something.",
                "text_reviews_count": 50,
                "ratings_count": 1500,
                "average_rating": 4.5,
                "id": 1,
                "authors": [
                    {"id": 1, "role": "Author"},
                    {"id": 2, "role": "Editor"}
                ]
            },
            {
                "title": "Book 2",
                "isbn": "0987654321",
                "isbn13": "0987654321123",
                "language": "English",
                "publisher": "Publisher 2",
                "publication_date": "2019-12-01",
                "format": "Paperback",
                "series_name": None,
                "series_position": None,
                "image_url": "http://example.com/book2.jpg",
                "description": "A second book description.",
                "text_reviews_count": 30,
                "ratings_count": 1200,
                "average_rating": 4.2,
                "id": 2,
                "authors": [
                    {"id": 1, "role": "Author"}
                ]
            }
        ]

        # Mock the pandas DataFrame chunks
        mock_chunks = [pd.DataFrame(mock_chunk_data)]  # Simulate chunked data from JSON

        # Set the mock to return the chunks
        mock_read_json.return_value = mock_chunks

        # Run the task
        import_books()

        # Assert that the books were created
        self.assertEqual(Book.objects.count(), 2)

        # Check that the first book was created correctly
        book1 = Book.objects.get(external_id=1)
        self.assertEqual(book1.name, "Book 1")
        self.assertEqual(book1.isbn, "1234567890")
        self.assertEqual(book1.ratings_count, 1500)

        # Check that the authors for the first book were linked correctly
        self.assertEqual(AuthorBook.objects.filter(book=book1).count(), 2)
        author_book1 = AuthorBook.objects.get(book=book1, author=self.author1)
        self.assertEqual(author_book1.role, "Author")
        author_book2 = AuthorBook.objects.get(book=book1, author=self.author2)
        self.assertEqual(author_book2.role, "Editor")

        # Check that the second book was created correctly
        book2 = Book.objects.get(external_id=2)
        self.assertEqual(book2.name, "Book 2")
        self.assertEqual(book2.isbn, "0987654321")

        # Check that the author for the second book was linked correctly
        self.assertEqual(AuthorBook.objects.filter(book=book2).count(), 1)
        author_book3 = AuthorBook.objects.get(book=book2, author=self.author1)
        self.assertEqual(author_book3.role, "Author")

    @patch('books.tasks.pd.read_json')  # Mock the pd.read_json function
    def test_import_books_with_empty_authors(self, mock_read_json):
        # Mock data with an empty authors list
        mock_chunk_data = [
            {
                "title": "Book 3",
                "isbn": "2222222222",
                "isbn13": "3333333333333",
                "language": "English",
                "publisher": "Publisher 3",
                "publication_date": "2021-06-15",
                "format": "eBook",
                "series_name": "Series B",
                "series_position": "2",
                "image_url": "http://example.com/book3.jpg",
                "description": "A book without authors.",
                "text_reviews_count": 10,
                "ratings_count": 500,
                "average_rating": 4.0,
                "id": 3,
                "authors": []  # Empty authors list
            }
        ]

        # Mock the pandas DataFrame chunks
        mock_chunks = [pd.DataFrame(mock_chunk_data)]  # Simulate chunked data from JSON

        # Set the mock to return the chunks
        mock_read_json.return_value = mock_chunks

        # Run the task
        import_books()

        # Assert that the book was created
        self.assertEqual(Book.objects.count(), 1)

        # Check that the book was created correctly
        book3 = Book.objects.get(external_id=3)
        self.assertEqual(book3.name, "Book 3")
        self.assertEqual(book3.isbn, "2222222222")
        self.assertEqual(book3.ratings_count, 500)

        # Ensure no authors were associated with this book
        self.assertEqual(AuthorBook.objects.filter(book=book3).count(), 0)
