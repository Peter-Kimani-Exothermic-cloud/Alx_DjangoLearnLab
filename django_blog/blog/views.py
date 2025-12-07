from django.shortcuts import render, get_object_or_404, redirect
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
from .models import Post,Comment
from .forms import PostForm
from .forms import CommentForm
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden


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



# --- Display Post and Handle New Comment (Creation) ---
# It's common to override the DetailView's get_context_data 
# and post methods to handle forms on the same page.
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # 1. Get the default context data
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # 2. Add the comment list (Display all comments)
        context['comments'] = post.comments.all() 
        
        # 3. Add the form for new comments (Creation)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        # This handles the form submission for a new comment
        self.object = self.get_object() # Get the current post object
        form = CommentForm(request.POST)

        if form.is_valid():
            # Only authenticated users can post comments
            if not request.user.is_authenticated:
                return redirect('login') # Or return HttpResponseForbidden

            # Create the comment object but don't save to database yet
            new_comment = form.save(commit=False)
            
            # Attach the foreign keys (post and author)
            new_comment.post = self.object
            new_comment.author = request.user
            
            # Save the new comment to the database
            new_comment.save()
            
            # Redirect to the same post detail page to show the new comment
            return redirect(self.object.get_absolute_url()) 
        
        # If form is invalid, re-render the page with errors
        context = self.get_context_data()
        context['comment_form'] = form # Pass the form with errors back to the template
        return self.render_to_response(context)


# --- Edit Comment (Update) ---
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_edit.html' # Create this template in Step 4

    def get_success_url(self):
        # Redirect back to the post detail page after successful edit
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # UserPassesTestMixin method: check if the user is the author
        comment = self.get_object()
        return self.request.user == comment.author

# --- Delete Comment (Delete) ---
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html' 
    context_object_name = 'comment'

    def get_success_url(self):
        # Redirect back to the post detail page after successful deletion
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        # UserPassesTestMixin method: check if the user is the author
        comment = self.get_object()
        return self.request.user == comment.author