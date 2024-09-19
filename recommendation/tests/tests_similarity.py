from django.test import TestCase
from unittest.mock import patch, MagicMock
from books.models import Book
from recommendation.models import BookFeature, BookSimilarity
from recommendation.tasks import calculate_similarity
import numpy as np
import pandas as pd
from scipy import sparse

class CalculateSimilarityTaskTestCase(TestCase):

    def setUp(self):
        # Set up test books
        self.book1 = Book.objects.create(
            name="Book about item 1", language="English", format="Hardcover", series_name="Series A", 
            about="A book about something", reviews_count=50, ratings_count=100, average_rating=4.5
        )
        self.book2 = Book.objects.create(
            name="Book about item 2", language="English", format="Paperback", series_name="Series A", 
            about="Another book about something", reviews_count=30, ratings_count=150, average_rating=4.0
        )
        self.book3 = Book.objects.create(
            name="Book about item 3", language="Spanish", format="eBook", series_name="Series B", 
            about="A different book", reviews_count=20, ratings_count=200, average_rating=3.5
        )

    @patch('recommendation.tasks.extract_vector_counter')  # Mock the feature extraction function
    @patch('recommendation.tasks.features_scaler')  # Mock the feature scaling function
    @patch('recommendation.tasks.cosine_similarity')  # Mock the cosine similarity calculation
    def test_calculate_similarity(self, mock_cosine_similarity, mock_features_scaler, mock_extract_vector_counter):
        # Mock the feature extraction and scaling for string and numeric features
        mock_extract_vector_counter.return_value = sparse.csr_matrix(np.array([
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0]
        ]))
        mock_features_scaler.return_value = np.array([
            [0.8],
            [0.5],
            [0.2]
        ])

        # Mock the cosine similarity output
        mock_cosine_similarity.return_value = np.array([
            [1.0, 0.9, 0.1],
            [0.9, 1.0, 0.3],
            [0.1, 0.3, 1.0]
        ])

        # Run the task
        calculate_similarity()

        # Check that the BookFeature table was populated correctly
        self.assertEqual(BookFeature.objects.count(), 3)
        book_feature1 = BookFeature.objects.get(book=self.book1)
        self.assertIsInstance(book_feature1.features, list)
        
        # Check that the BookSimilarity table was populated correctly
        self.assertEqual(BookSimilarity.objects.count(), 6)  # 3 books, 2 similarity records per book (ignoring self)
        
        # Check similarity values for book1
        book_similarity1 = BookSimilarity.objects.filter(book_base=self.book1)
        self.assertEqual(book_similarity1.count(), 2)
        

        # Check similarity values for book2
        book_similarity2 = BookSimilarity.objects.filter(book_base=self.book2)
        self.assertEqual(book_similarity2.count(), 2)