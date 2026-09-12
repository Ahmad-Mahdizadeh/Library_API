from rest_framework import serializers
from .models import Author,Book,Borrow

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id','first_name','last_name','bio')


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ('id','title','author_name','author','isbn','is_available','created_at')
        read_only_fields = ('id','is_available','created_at')
    def get_author_name(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'

class BorrowSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source ='book.title')
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Borrow
        fields = ('id','book','book_title','user','username','borrowed_at','returned_at')
        read_only_fields = ('id','user','borrowed_at','returned_at')
