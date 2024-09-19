from django.conf import settings
import pandas as pd

from settings.celery import app
from authors.models import Author

@app.task(bind=True)
def import_authors(self):
    FILE_PATH="/code/.ignore/assets/authors.json/authors.json"
    CHUNKSIZE=500
    MAX_CHUNKS=10
    i=0
    chunks = pd.read_json(FILE_PATH, lines=True, chunksize = CHUNKSIZE)
    for chunk in chunks:
        i+=1
        if i>MAX_CHUNKS:
            break
        Author.objects.bulk_create([
            Author(
                name = row["name"],
                gender = row["gender"],
                image_url = row["image_url"],
                about = row["about"],
                reviews_count = row["text_reviews_count"],
                fans_count = row["fans_count"],
                ratings_count = row["ratings_count"],
                average_rating =row["average_rating"],
                external_id = row["id"]
            ) for _,row in chunk.iterrows()
        ])