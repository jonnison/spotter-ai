from rest_framework import serializers
from django.db.models import Sum

from books.serializers import BookSerializer
from books.models import Book
from recommendation.models import Favorite, BookSimilarity

class FavoriteSerializer(serializers.ModelSerializer):
    recommended_books = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at','user']

    def validate_book(self,value):
        if Favorite.objects.filter(user=self.context["request"].user,book=value):
            raise serializers.ValidationError(
                "This book is already in your favorite list"
            )
        return value

    def validate(self, attrs):

        if Favorite.objects.filter(user=self.context["request"].user).count() > 20:
            raise serializers.ValidationError(
                "Favorite list limit exceeded"
            )
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    def get_recommended_books(self, obj):
        favorite_list = Favorite.objects.filter(user = self.context["request"].user).values('book__id')
        recommendation_list = BookSimilarity.objects.filter(book_base__in=favorite_list).values("book_related").annotate(
            similarity_agg=Sum("similarity")
        ).order_by("-similarity_agg").values_list("book_related",flat=True)[:5]
        return BookSerializer(Book.objects.filter(id__in=recommendation_list),many=True).data
