from django.shortcuts import render
from .models import Book
from rest_framework import generics
from .serializers import BookSerializer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


#CRUD 
# ---------------------------------------------------
#List all books, search, ordering
#Anyone can read
# ---------------------------------------------------

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    

    #FILTERING, SEARCING, ORDERING
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    #Filtering
    filter_fields = ['title', 'author', 'publication_year']

    #Searching
    search_fields = ['title', 'author_name']

    #Ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  #default ordering


#Retrieve a single book
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

#Create a book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    

#Update a Book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

#Delete a Book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]









