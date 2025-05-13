from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# from .forms import CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import reverse_lazy

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')  # Redirect to main library view
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'accounts/password_reset.html'
#     # email_template_name = 'accounts/password_reset_email.html'  # Optional
#     # subject_template_name = 'accounts/password_reset_subject.txt'  # Optional
#     success_url = reverse_lazy('password_reset_done')
# class CustomPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'accounts/password_reset_done.html'
# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'accounts/password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')
# class CustomPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'accounts/password_reset_complete.html'
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get the username from the form
        if username:
            try:
                user = User.objects.get(username=username)  # Try to get the user by username
                return redirect('change_password', user_id=user.id)  # Redirect to change password page with user ID
            except User.DoesNotExist:
                messages.error(request, "No user found with this username")
        else:
            messages.error(request, "Username field cannot be empty")

    return render(request, 'accounts/forgot_password.html')
@login_required
def change_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)  # Retrieve the user by ID
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')  # Redirect to login if user is not found

    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been successfully updated.")
            return redirect('login')  # After changing password, redirect to login page
    else:
        form = PasswordChangeForm(user=user)

    return render(request, 'accounts/change_password.html', {'form': form})
def password_change_done(request):
    return render(request, 'library/password_change_done.html')
