from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm, ProfileExtraForm

def register(request):
    if request.method == 'POST':       #Checks if user has submitted form
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():            #checks if everything is okay(passwords matc, email valid, etc)
            user = form.save()         #save user to DB
            login(request, user)       #Automatically log them immediately
            messages.success(request, "Registration successful. You're logged in")
            return redirect('profile')    #Redirect to home/profile

    else:
        form = CustomUserCreationForm()   
    
    return render(request, 'blog/register.html', {'form': form} )  

@login_required  
def profile_view(request):
    """
    Display user profile and allow updates for username and optional Profile fields
    """
    user = request.user

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        profile_form = None
        if hasattr(user, 'profile'):
            profile_form = ProfileExtraForm(request.POST, request.FILES, instance=user.profile)  

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profile')
    
    else:
        user_form = ProfileUpdateForm(instance=user)
        profile_form = ProfileExtraForm(instance=user.profile) if hasattr(user, 'profile') else None
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'blog/profile.html', context)








