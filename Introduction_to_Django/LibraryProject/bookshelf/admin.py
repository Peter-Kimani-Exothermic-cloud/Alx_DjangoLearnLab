from django.contrib import admin

# 1. Import the model you want to manage from the current app's models file
from .models import Book

# Register your models here.
@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'publication_year')  # Columns to show in list view
        list_filter = ('publication_year', 'author')             # Filters on the right sidebar
        search_fields = ('title', 'author')                      # Search box fields
    
   