from rest_framework import serializers
from .models import Book,Author
import datetime

class BookSerializer(serializers.ModelSerializer):  
    def validate_publication_year(self,data):
        current_publication = datetime.date.today().year
        if current_publication > data:
            raise serializers.ValidationError(f"Publication year cannot be in the future. ({data})")
        return data

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only = True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


    