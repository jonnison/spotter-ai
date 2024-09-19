from rest_framework import serializers
from books.models import Book, AuthorBook
from recommendation.tasks import calculate_similarity



class AuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorBook
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at','book']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorBookSerializer(many=True)
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):

        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        for item in authors_data:
            item["book"]=book
            
        AuthorBook.objects.bulk_create([AuthorBook(**item) for item in authors_data])
        calculate_similarity.delay()
        return book