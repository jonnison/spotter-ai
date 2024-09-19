from django.test import TestCase
from django_filters import rest_framework as filters
from authors.models import Author
from authors.filters import AuthorFilter

class AuthorFilterTestCase(TestCase):

    def setUp(self):
        # Create some author instances for testing
        self.author1 = Author.objects.create(
            name="John Smith",
            about="Fiction writer known for his mystery novels."
        )
        self.author2 = Author.objects.create(
            name="Jane Doe",
            about="Non-fiction author focused on history and science."
        )
        self.author3 = Author.objects.create(
            name="Smith Johnson",
            about="Writes about nature and environmental issues."
        )

    def test_filter_by_name(self):
        # Filter authors with 'Smith' in their name
        data = {'name': 'Smith'}
        author_filter = AuthorFilter(data=data, queryset=Author.objects.all())
        filtered_authors = author_filter.qs

        # Expect to get the authors with 'Smith' in their names
        self.assertEqual(filtered_authors.count(), 2)
        self.assertIn(self.author1, filtered_authors)
        self.assertIn(self.author3, filtered_authors)

    def test_filter_by_search(self):
        # Search for 'science' in either name or about
        data = {'search': 'science'}
        author_filter = AuthorFilter(data=data, queryset=Author.objects.all())
        filtered_authors = author_filter.qs

        # Expect to get only Jane Doe who mentions 'science' in her 'about'
        self.assertEqual(filtered_authors.count(), 1)
        self.assertIn(self.author2, filtered_authors)

    def test_filter_by_name_and_search(self):
        # Filter by name 'Smith' and search for 'mystery'
        data = {'name': 'Smith', 'search': 'mystery'}
        author_filter = AuthorFilter(data=data, queryset=Author.objects.all())
        filtered_authors = author_filter.qs

        # Expect to get John Smith because he fits both filters
        self.assertEqual(filtered_authors.count(), 1)
        self.assertIn(self.author1, filtered_authors)

    def test_empty_filter(self):
        # Test an empty filter
        data = {}
        author_filter = AuthorFilter(data=data, queryset=Author.objects.all())
        filtered_authors = author_filter.qs

        # Expect to get all authors
        self.assertEqual(filtered_authors.count(), 3)
        self.assertIn(self.author1, filtered_authors)
        self.assertIn(self.author2, filtered_authors)
        self.assertIn(self.author3, filtered_authors)

    def test_no_results_filter(self):
        # Filter by a name that doesn't exist
        data = {'name': 'Nonexistent'}
        author_filter = AuthorFilter(data=data, queryset=Author.objects.all())
        filtered_authors = author_filter.qs

        # Expect to get no results
        self.assertEqual(filtered_authors.count(), 0)

