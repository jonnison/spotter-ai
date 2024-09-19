from django.db import models
from django.contrib.auth.models import User

from base.models import BaseModel
from books.models import Book

class Favorite(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

class BookFeature(BaseModel):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    features = models.JSONField()

class BookSimilarity(BaseModel):
    book_base = models.ForeignKey(Book,on_delete=models.CASCADE , related_name="books")
    book_related = models.ForeignKey(Book,on_delete=models.CASCADE, related_name="books_related")
    similarity = models.DecimalField(max_digits=20,decimal_places=10)