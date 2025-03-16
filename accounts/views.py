from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.models import CustomUser
from .forms import CustomUserCreationForm, CustomLoginForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied


# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a success page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required(login_url='login_view')
def add_user_view(request):
    if not request.user.is_owner(): # Only owner can add users
        raise PermissionDenied
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 == password2:
                form.save()
                messages.success(request, 'User added successfully.')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Form is not valid. Weak password.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/add_user.html', {'form': form})

@login_required(login_url='login_view')
def dashboard_view(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/dashboard.html', {'users': users})

@login_required(login_url='login_view')
def users_view(request):
    if not request.user.is_owner(): # Only owner can view users
        raise PermissionDenied
    users = CustomUser.objects.filter(is_superuser=False)   #   Exclude superusers from displayingin frontend
    if request.method == 'POST':
        if 'edit_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, pk=user_id)
            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'User updated successfully.')
                return redirect('users')
            else:
                messages.error(request, 'Failed to update user. Please correct the errors below.')
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, pk=user_id)
            user.delete()
            messages.success(request, 'User deleted successfully.')
            return redirect('users')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/users.html', {'users': users, 'form': form})


