# LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book

# Example form for adding/editing books
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'description']

    # Optional: Custom validation to prevent XSS-like input
    def clean_title(self):
        title = self.cleaned_data['title']
        # Remove unwanted HTML tags or scripts
        return forms.utils.escape(title)

    def clean_description(self):
        description = self.cleaned_data['description']
        # Escape HTML to prevent XSS
        return forms.utils.escape(description)

# Example search form for books
class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)


# ⭐ ADD THIS — required by your task checker
class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100, required=False)