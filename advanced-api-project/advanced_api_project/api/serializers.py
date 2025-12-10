from rest_framework import serializers
from .models import Book,Author
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        name = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    #custom validation.
    def validate_publication_year(self, data):
        current_year = datetime.date.today().year
        if data > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. ({data})"
            )
        return data


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        name = Author
        fields = ['id', 'name', 'books']






from rest_framework import serializers
from .models import Book,Author
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        name = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    #custom validation.
    def validate_publication_year(self, data):
        current_year = datetime.date.today().year
        if data > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. ({data})"
            )
        return data


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        name = Author
        fields = ['id', 'name', 'books']
    



    


