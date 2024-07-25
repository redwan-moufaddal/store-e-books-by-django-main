from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def register(request):
    if request.user.is_authenticated:
        return redirect('base:home')  # Redirect to home page if already logged in

    if request.method == 'POST':
        if 'register' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()  # Create new user
                user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                    return redirect('base:home')  # Redirect to home page after login
                else:
                    # Handle incorrect authentication after registration
                    messages.error(request, 'Invalid username or password after registration.')
                    # Consider providing more specific error messages
                    return render(request, 'registration/register.html', {'form': form})
            else:
                # Handle registration form errors
                messages.error(request, 'Registration form has errors.')
                # Consider providing specific error messages for each field
                return render(request, 'registration/register.html', {'form': form})
        elif 'login' in request.POST:
            # Handle login attempt
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('base:home')  # Redirect to home page after login
            else:
                messages.error(request, 'Invalid username or password for login.')
                # Consider providing more specific error messages
                return render(request, 'registration/register.html', {'error': 'Invalid credentials'})

    form = RegisterForm()  # Create new form instance
    return render(request, 'registration/register.html', {'form': form})

def logout_user(request):
    logout(request)
    # Redirect to a specific page after logout (you can customize the URL)
    return redirect('base:home')

def add_review(request):
    email = request.POST.get('email')
    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse("This email alrady exists")
    else:
        return HttpResponse("This email is available")