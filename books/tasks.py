from django.conf import settings
import pandas as pd

from settings.celery import app
from authors.models import Author
from books.models import Book,AuthorBook

@app.task(bind=True)
def import_books(self):
    FILE_PATH="/code/.ignore/assets/books.json/books.json"
    CHUNKSIZE=500
    MAX_CHUNKS=10
    i=0
    chunks = pd.read_json(FILE_PATH, lines=True, chunksize = CHUNKSIZE)
    for chunk in chunks:
        i+=1
        if i>MAX_CHUNKS:
            break
        try:
            for _,row in chunk.iterrows():
                book = Book.objects.create(
                    name = row["title"],
                    isbn = row["isbn"],
                    isbn13 = row["isbn13"],
                    language = row["language"],
                    publisher = row["publisher"],
                    publication_date = row["publication_date"] if len(row["publication_date"])==10 else None, 
                    format = row["format"],
                    series_name = row["series_name"],
                    series_position = row["series_position"],
                    image_url = row["image_url"],
                    about = row["description"],
                    reviews_count = row["text_reviews_count"],
                    ratings_count = row["ratings_count"],
                    average_rating = row["average_rating"],
                    external_id = row["id"],
                )
                if isinstance(row["authors"],list):
                    for author in row["authors"]:
                        if(Author.objects.filter(external_id=author["id"]).exists()):
                            author_instance = Author.objects.filter(external_id=author["id"]).first()
                            AuthorBook.objects.create(
                                author=author_instance,
                                book=book,
                                role=author["role"]
                            )
        except Exception:
            pass

        