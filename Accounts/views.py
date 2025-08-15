from webbrowser import register

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from Accounts.forms import RegisterUserForm, LoginForm, UpdateUserForm, UpdateProfileForm


# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'add_form.html', {'form': form, 'form_type':'register'})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, username=username, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user)  # log the user in
                return redirect('home')  # redirect to homepage or dashboard
        return render(request, 'add_form.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'add_form.html', {'form': form, 'form_type':'login'})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user= authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        return render(request, 'add_form.html', {'form': form, 'error':'datos incorrectos'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})