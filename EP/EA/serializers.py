from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):
        # Проверка, является ли книга учебником:
        if attrs['category'] == Book.TEXTBOOK:
            if Book.objects.filter(title=attrs['title'], author=attrs['author'], publisher=attrs['publisher'],
                                   year=attrs['year']).exists():
                raise serializers.ValidationError("Учебник с таким издательством и годом издания уже существует.")
        return attrs


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def validate(self, attrs):
        if Author.objects.filter(first_name=attrs['first_name'], last_name=attrs['last_name']).exists():
            raise serializers.ValidationError("Автор с таким именем уже существует.")
        return attrs