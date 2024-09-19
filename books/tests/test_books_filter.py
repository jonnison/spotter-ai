from django.test import TestCase
from django_filters import rest_framework as filters
from books.models import Book, Author
from books.filters import BookFilter

class BookFilterTestCase(TestCase):

    def setUp(self):
        # Create authors
        self.author1 = Author.objects.create(name="John Smith")
        self.author2 = Author.objects.create(name="Jane Doe")
        
        # Create books with these authors
        self.book1 = Book.objects.create(name="Mystery of the Lost Island")
        self.book1.authors.add(self.author1)

        self.book2 = Book.objects.create(name="Science and Space")
        self.book2.authors.add(self.author2)

        self.book3 = Book.objects.create(name="The Nature of the Universe")
        self.book3.authors.add(self.author1, self.author2)

    def test_filter_by_name(self):
        # Test filtering by name field
        data = {'name': 'Mystery'}
        book_filter = BookFilter(data=data, queryset=Book.objects.all())
        filtered_books = book_filter.qs

        # Expect to get the book that contains 'Mystery' in the name
        self.assertEqual(filtered_books.count(), 1)
        self.assertIn(self.book1, filtered_books)

    def test_filter_by_search_book_name(self):
        # Test filtering by search field which searches in book name
        data = {'search': 'Space'}
        book_filter = BookFilter(data=data, queryset=Book.objects.all())
        filtered_books = book_filter.qs

        # Expect to get the book that contains 'Space' in the name
        self.assertEqual(filtered_books.count(), 1)
        self.assertIn(self.book2, filtered_books)

    def test_filter_by_search_author_name(self):
        # Test filtering by search field which searches in author name
        data = {'search': 'John'}
        book_filter = BookFilter(data=data, queryset=Book.objects.all())
        filtered_books = book_filter.qs

        # Expect to get books by author 'John Smith'
        self.assertEqual(filtered_books.count(), 2)
        self.assertIn(self.book1, filtered_books)
        self.assertIn(self.book3, filtered_books)

    def test_filter_by_name_and_search(self):
        # Test filtering by both name and search field
        data = {'name': 'Nature', 'search': 'Doe'}
        book_filter = BookFilter(data=data, queryset=Book.objects.all())
        filtered_books = book_filter.qs

        # Expect to get the book that contains 'Nature' in the name and 'Doe' in author name
        self.assertEqual(filtered_books.count(), 1)
        self.assertIn(self.book3, filtered_books)

    def test_empty_filter(self):
        # Test that applying no filters returns all books
        data = {}
        book_filter = BookFilter(data=data, queryset=Book.objects.all())
        filtered_books = book_filter.qs

        # Expect to get all books
        self.assertEqual(filtered_books.count(), 3)
        self.assertIn(self.book1, filtered_books)
        self.assertIn(self.book2, filtered_books)
        self.assertIn(self.book3, filtered_books)

    def test_no_results_filter(self):
        # Test that filtering by a name that doesn't exist returns no books
        data = {'name': 'Nonexistent'}
        book_filter = BookFilter(data=data, queryset=Book.objects.all())
        filtered_books = book_filter.qs

        # Expect no results
        self.assertEqual(filtered_books.count(), 0)

