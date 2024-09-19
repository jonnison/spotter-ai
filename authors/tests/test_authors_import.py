from django.test import TestCase
import pandas as pd
from unittest.mock import patch, MagicMock
from authors.models import Author
from settings.celery import app
from authors.tasks import import_authors

class ImportAuthorsTaskTestCase(TestCase):
    
    @patch('authors.tasks.pd.read_json')  # Mock pandas read_json function
    def test_import_authors(self, mock_read_json):
        # Mock data as if read from a JSON file
        mock_chunk_data = [
            {
                "name": "John Smith",
                "gender": "male",
                "image_url": "http://example.com/image.jpg",
                "about": "An author of several bestsellers.",
                "text_reviews_count": 100,
                "fans_count": 200,
                "ratings_count": 1500,
                "average_rating": 4.5,
                "id": 1
            },
            {
                "name": "Jane Doe",
                "gender": "female",
                "image_url": "http://example.com/janedoe.jpg",
                "about": "A renowned non-fiction author.",
                "text_reviews_count": 150,
                "fans_count": 300,
                "ratings_count": 2000,
                "average_rating": 4.7,
                "id": 2
            }
        ]
        
        # Mock pandas chunks
        mock_chunks = [pd.DataFrame(mock_chunk_data)]  # Mock a list of DataFrames for chunks

        # Set up the mock to return the chunks
        mock_read_json.return_value = mock_chunks
        
        # Run the Celery task
        import_authors()

        # Assert that two authors were created
        self.assertEqual(Author.objects.count(), 2)
        
        # Assert that the data was correctly inserted into the Author model
        author1 = Author.objects.get(external_id=1)
        self.assertEqual(author1.name, "John Smith")
        self.assertEqual(author1.gender, "male")
        self.assertEqual(author1.image_url, "http://example.com/image.jpg")
        self.assertEqual(author1.reviews_count, 100)
        self.assertEqual(author1.fans_count, 200)
        self.assertEqual(author1.ratings_count, 1500)
        
        author2 = Author.objects.get(external_id=2)
        self.assertEqual(author2.name, "Jane Doe")
        self.assertEqual(author2.gender, "female")
        self.assertEqual(author2.image_url, "http://example.com/janedoe.jpg")
        self.assertEqual(author2.reviews_count, 150)
        self.assertEqual(author2.fans_count, 300)
        self.assertEqual(author2.ratings_count, 2000)

