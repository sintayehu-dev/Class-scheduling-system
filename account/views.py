from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms1 import LoginForm, UserRegistrationForm



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

##################################################

def user_list(request):
    users = User.objects.all()
    return render(request, 'account/user_list.html', {'users': users})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('user_list')

def update_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.username = request.POST.get('username')
        user.save()
        return redirect('user_list')  # Redirect to the user list page after update
    else:
        user = get_object_or_404(User, pk=user_id)
        return redirect(reverse('update_user_page', kwargs={'user_id': user_id}))

def update_user_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'account/update_user.html', {'user': user})

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Hardcoded usernames and passwords
        hardcoded_credentials = {
            'admin': 'password',
            # 'user2': 'password2',
            # Add more users as needed
        }
        
        if username in hardcoded_credentials and hardcoded_credentials[username] == password:
            # Authentication successful
            messages.success(request, "Login successful!")
            return redirect('index1')  # Redirect to home page after login
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password.")
    return render(request, 'account/adminlogin.html')

