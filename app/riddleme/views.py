from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from .models import Submitted, Puzzle, PuzzleStatistics
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, 'riddleme/index.html')

def page(request, page_num):
    puzzles = Puzzle.objects.all().order_by('id')
    
    paginator = Paginator(puzzles, per_page=6)
    page_obj = paginator.get_page(page_num)
    
    context = {
        "page_obj": page_obj
        }
    return render(request, 'riddleme/page.html', context)

def puzzle(request, puzzle_id):
    return HttpResponse(f"You're accessing puzzle {puzzle_id}")

def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        
        submit_count = Submitted.objects.filter(uid=user.id).count()
        
        solved_count = Submitted.objects.filter(uid=user.id, correct=True) \
                                .order_by('pid').values('pid').distinct().count()
        
        puzzle_list = Submitted.objects.filter(uid=user.id, correct=True).order_by('date').select_related('pid')
        plist = [{
            "puzzle_title":entry.pid.title,
            "puzzle_id": entry.pid.id,
            "date": entry.date,
          } for entry in puzzle_list]
        
        context = {
            "creation_date": user.date_joined,
            "solved_puzzles": solved_count,
            "submitted_count": submit_count,
            "last_activity": user.last_login,
            "puzzle_list": plist
        }
        return render(request, 'riddleme/profile.html', context)
    else:
        return redirect('index')

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