from multiprocessing.spawn import import_main_path
from operator import imod
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'riddleme/index.html')

def page(request, page_num):
    return HttpResponse(f"You're on page {page_num}")

def puzzle(request, puzzle_id):
    return HttpResponse(f"You're accessing puzzle {puzzle_id}")

def user_profile(request):
    return render(request, 'riddleme/profile.html')

def login_user(request):
    from django.contrib.auth import authenticate, login
    
    if request.method == 'POST':
        # processing logging request
        username = request.POST['username']
        password = request.POST['password']
        # check if user exists
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # save session as cookie
            login(request, user)
            # send message about log in
            messages.success(request, f"Zalogowano poprawnie na użytkownika: {username}.")
            # redirect to index or profile page
            return redirect('index')
        else:
            # wrong credentials
            messages.error(request, f"Nazwa użytkownika lub hasło jest niepoprawne, spróbuj ponownie.")
            # render again
            return render(request, 'riddleme/login.html')            
    else:
        # render normal login page
        return render(request, 'riddleme/login.html')

def logout_user(request):
    from django.contrib.auth import logout
    
    logout(request)
    messages.success(request, "Poprawnie wylogowano użytkownika.")
    return redirect('index')

def register_user(request):
    from .forms import RegisterForm
    from django.contrib.auth.models import User
    from django.contrib.auth import login
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        # check form validity
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Użytkownik o tej nazwie już istnieje.")
                return render(request, 'riddleme/register.html', {'form': form})
            if not password_check(form.cleaned_data['password']):
                messages.error(request, "Hasło nie spełnia wymagań.")
                return render(request, 'riddleme/register.html', {'form': form})
            if form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                messages.error(request, "Podane hasła nie są jednakowe.")
                return render(request, 'riddleme/register.html', {'form': form})
            
            user = User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password'])
            user.save()
            
            login(request, user)
            
            messages.success(request, f"Udało się zarejestrować użytkownika: {user.username}")
            
            return redirect('index')
    else:
        form = RegisterForm()
    
    return render(request, 'riddleme/register.html', {'form': form})

def password_check(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    return True