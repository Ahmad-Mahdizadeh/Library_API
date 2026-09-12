from django.utils import timezone
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Author,Book,Borrow
from .serializers import AuthorSerializer,BookSerializer, BorrowSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_available","author"]
    search_fields = ["title","isbn"]
    @action(detail=True,methods=["post"])
    def borrow(self,request,pk=None):
        book = self.get_object()
        if not book.is_available:
            return Response({"detail":"This book is already borrowed"},status=status.HTTP_400_BAD_REQUEST)
        borrow = Borrow.objects.create(book=book,user=request.user)
        book.is_available = False
        book.save()
        return Response(BorrowSerializer(borrow).data,status=status.HTTP_201_CREATED)
    @action(detail=True,methods=["post"])
    def return_book(self,request,pk=None):
        book = self.get_object()
        borrow = Borrow.objects.filter(book=book,
                                       user=request.user,
                                    returned_at__isnull=True).first()
        if not borrow:
            return Response({"detail":"You have no active borrow for this book"},
                            status=status.HTTP_400_BAD_REQUEST)
        borrow_returned_at = timezone.now
        borrow.save(update_fields=["returned_at"])
        book.is_available = True
        book.save(update_fields=["is_available"])
        return Response(BorrowSerializer(borrow).data,status=status.HTTP_201_CREATED)

class BorrowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).select_related("book","user")





# Create your views here.
