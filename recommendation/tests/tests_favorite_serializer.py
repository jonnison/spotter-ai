from django.test import TestCase
from unittest.mock import patch
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from books.models import Book
from recommendation.models import Favorite, BookSimilarity
from books.serializers import BookSerializer
from recommendation.serializers import FavoriteSerializer
from django.contrib.auth.models import User

class FavoriteSerializerTestCase(TestCase):

    def setUp(self):
        # Create a user and books for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book1 = Book.objects.create(name="Book 1")
        self.book2 = Book.objects.create(name="Book 2")
        self.book3 = Book.objects.create(name="Book 3")

        # Create an API request factory
        self.factory = APIRequestFactory()
        self.request = self.factory.post('/fake-url/')
        self.request.user = self.user

    def test_validate_book_already_favorite(self):
        # Add a book to the user's favorite list
        Favorite.objects.create(user=self.user, book=self.book1)

        # Test validation that book is already in favorites
        serializer = FavoriteSerializer(data={"book": self.book1.id}, context={"request": self.request})
        
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertEqual(str(context.exception.detail["book"][0]), "This book is already in your favorite list")

    def test_validate_favorite_list_limit_exceeded(self):
        # Add 20 books to the user's favorite list
        for i in range(1, 22):
            book = Book.objects.create(name=f"Book {i}")
            Favorite.objects.create(user=self.user, book=book)
        
        # Try adding another book and expect the limit error
        serializer = FavoriteSerializer(data={"book": self.book1.id}, context={"request": self.request})
        
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(str(context.exception.detail['non_field_errors'][0]), "Favorite list limit exceeded")

    def test_create_favorite(self):
        # Test creating a favorite instance
        serializer = FavoriteSerializer(data={"book": self.book1.id}, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        favorite = serializer.save()

        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.book, self.book1)

    @patch('recommendation.serializers.BookSerializer')  # Mock BookSerializer
    def test_get_recommended_books(self, mock_book_serializer):
        # Set up mock for recommended books
        Favorite.objects.create(user=self.user, book=self.book1)
        Favorite.objects.create(user=self.user, book=self.book2)

        # Create some book similarity data
        BookSimilarity.objects.create(book_base=self.book1, book_related=self.book3, similarity=0.9)

        # Mock BookSerializer response
        mock_book_serializer.return_value.data = [{"name": "Book 3"}]

        # Test recommended books
        favorite = Favorite.objects.get(book=self.book1)
        serializer = FavoriteSerializer(instance=favorite, context={"request": self.request})

        recommended_books = serializer.data['recommended_books']
        
        self.assertEqual(recommended_books, [{"name": "Book 3"}])
        mock_book_serializer.assert_called_once()

