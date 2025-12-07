from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import(
    ListView,DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


#LIST VIEW - Show all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

#DETAILVIEW - Show individual blog posts
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

#CREATE VIEW -Authenticated users only
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#UPDATE VIEW -Only author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

#DELETE VIEW - Only author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



#Registration of customview
# Registration View (Step 1)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

# Profile Management View (Step 4)
@login_required # Ensures only logged-in users can access this (Step 5)
def profile(request):
    if request.method == 'POST':
        # Pass the request.user instance to both forms
        # request.FILES handles the image upload
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated successfully! ✨')
            return redirect('profile') 
    else:
        # Load current data into forms for GET request
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'User Profile'
    }

    return render(request, 'blog/profile.html', context)