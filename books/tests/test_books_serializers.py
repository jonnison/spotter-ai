from django.test import TestCase
from rest_framework.exceptions import ValidationError
from books.models import Book, AuthorBook
from authors.models import Author
from books.serializers import BookSerializer, AuthorBookSerializer

class BookSerializerTestCase(TestCase):

    def setUp(self):
        # Set up an author for testing
        self.author1 = Author.objects.create(name="Author 1")
        self.author2 = Author.objects.create(name="Author 2")


        # Book instance
        self.book = Book.objects.create(name="Test Book", about="A sample about")

        # AuthorBook entries
        self.author_book1 = AuthorBook.objects.create(author=self.author1,book=self.book)
        self.author_book2 = AuthorBook.objects.create(author=self.author2,book=self.book)

    def test_author_book_serializer(self):
        """Test serialization of AuthorBook model"""
        serializer = AuthorBookSerializer(instance=self.author_book1)
        data = serializer.data
        
        self.assertEqual(data['author'], self.author1.id)
        self.assertIn('created_at', data)  # Should be present but read-only
        self.assertIn('updated_at', data)  # Should be present but read-only

    def test_book_serializer(self):
        """Test serialization of Book model with nested authors"""
        book_data = {
            "name": "New Book",
            "about": "This is a new book",
            "authors": [
                {"author": self.author1.id},
                {"author": self.author2.id}
            ]
        }

        # Serialize data
        serializer = BookSerializer(data=book_data)
        self.assertTrue(serializer.is_valid())

        # Save the new book and authors
        book = serializer.save()

        self.assertEqual(book.name, "New Book")
        self.assertEqual(book.about, "This is a new book")
        self.assertEqual(book.authors.count(), 2)

        # Check that the authors are correctly associated with the book
        self.assertTrue(AuthorBook.objects.filter(book=book, author=self.author1).exists())
        self.assertTrue(AuthorBook.objects.filter(book=book, author=self.author2).exists())

    def test_book_serializer_invalid_data(self):
        """Test book serializer with invalid nested authors data"""
        invalid_data = {
            "name": "Invalid Book",
            "about": "This book has invalid authors",
            "authors": [
                {"author": None}  # Invalid author
            ]
        }

        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('authors', serializer.errors)

    def test_create_method(self):
        """Test that the create method properly handles the authors data"""
        book_data = {
            "name": "Created Book",
            "about": "This is a created book",
            "authors": [
                {"author": self.author1.id},
                {"author": self.author2.id}
            ]
        }

        # Test create method
        serializer = BookSerializer(data=book_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        
        book = serializer.save()
        
        self.assertEqual(book.name, "Created Book")
        self.assertEqual(book.about, "This is a created book")
        self.assertEqual(AuthorBook.objects.filter(book=book).count(), 2)

        # Verify that the authors were correctly associated with the book
        self.assertTrue(AuthorBook.objects.filter(book=book, author=self.author1).exists())
        self.assertTrue(AuthorBook.objects.filter(book=book, author=self.author2).exists())

