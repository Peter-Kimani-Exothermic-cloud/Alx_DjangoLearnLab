from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post

# Custom Registration Form to include email
class CustomUserCreationForm(UserCreationForm):
    # The email field is a standard User model field, but UserCreationForm 
    # does not include it by default, so we add it here.
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email') + UserCreationForm.Meta.fields[2:] 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Form for editing the core User fields (username and email)
class UserUpdateForm(UserChangeForm):
    password = None # Don't allow password change in this form

    class Meta:
        model = User
        fields = ('username', 'email')



#Profile update form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

#Post form
# Ensure the class name is exactly 'PostForm'
class PostForm(forms.ModelForm):
    # ... form code
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']

