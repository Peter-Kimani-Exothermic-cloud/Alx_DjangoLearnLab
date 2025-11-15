from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import  Library
from .models import Book




#Function based view (FBV) to list all books

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

#Class based view (CBV) to show details of a specific library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

