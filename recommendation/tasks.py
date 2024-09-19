from django.conf import settings
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

from settings.celery import app
from books.models import Book
from recommendation.models import BookFeature, BookSimilarity

def extract_vector_counter(corpus):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    return X
def features_scaler(features):
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    return features_scaled


@app.task(bind=True)
def calculate_similarity(self):
    #clear features and recommendations tables
    BookFeature.objects.all().delete()
    BookSimilarity.objects.all().delete()

    books_qs = Book.objects.order_by("id").all()

    #extracting all features
    #string features
    name_features = extract_vector_counter(books_qs.values_list("name", flat=True))
    language_features = extract_vector_counter(books_qs.values_list("language", flat=True))
    format_features = extract_vector_counter(books_qs.values_list("format", flat=True))
    series_name_features = extract_vector_counter(books_qs.values_list("series_name", flat=True))
    about_features = extract_vector_counter(books_qs.values_list("about", flat=True))
    
    #numeric features
    reviews_features = features_scaler(np.array(books_qs.values_list("reviews_count", flat=True)).reshape(-1,1))
    ratings_features = features_scaler(np.array(books_qs.values_list("ratings_count", flat=True)).reshape(-1,1))
    average_features = features_scaler(np.array(books_qs.values_list("average_rating", flat=True)).reshape(-1,1))
    #convert to sparse matrix
    reviews_features = sparse.csr_matrix(reviews_features)
    ratings_features = sparse.csr_matrix(ratings_features)
    average_features = sparse.csr_matrix(average_features)

    #combine all features
    combined_features = sparse.hstack([
        name_features, 
        language_features,
        format_features,
        series_name_features,
        about_features,
        reviews_features,
        ratings_features,
        average_features,
    ])

    # Calculate cosine similarity between all books
    cosine_sim = cosine_similarity(combined_features)
    
    #Saving similarity
    book_list = list(books_qs)

    #Populate Similarity
    for i in range(cosine_sim.shape[0]):
        create = []
        for j in range(cosine_sim.shape[1]):
            # ignore similarity for same book
            if i==j:
                continue
            create.append(BookSimilarity(
                book_base=book_list[i],
                book_related=book_list[j],
                similarity=cosine_sim[i,j]
            ))
        BookSimilarity.objects.bulk_create(create,batch_size=100)
            

    #Populate Features
    for i,book in enumerate(book_list):
        BookFeature.objects.create(
            book=book,
            features=combined_features[i].toarray().tolist()
        ) 
