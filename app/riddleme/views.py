from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Submitted, Puzzle, PuzzleStatistics, default_datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.timezone import localtime
from django.utils import timezone

# Create your views here.
def index(request):
    puzzle_count = Puzzle.objects.all().count()
    unsolved_count = PuzzleStatistics.objects.filter(first_solve=default_datetime).count()
    
    context = {
        "puzzle_count": puzzle_count,
        "unsolved_count": unsolved_count,
    }
    return render(request, 'riddleme/index.html', context)

def page(request, page_num):
    puzzles = Puzzle.objects.all().order_by('-id')
    user_count = User.objects.all().count()
    puzzle_list = []
    for puzzle in puzzles:
        stats = PuzzleStatistics.objects.get(pid=puzzle)
        solved = False
        if request.user.is_authenticated:
            user = request.user
            if Submitted.objects.filter(uid=user, correct=True, pid=puzzle).exists():
                solved = True
        puzzle_entry = {
            "puzzle_id": puzzle.id,
            "puzzle_title": puzzle.title,
            "solved": solved,
            "solve_ratio": str(round((stats.solved_count/float(user_count)) * 100)) + "%",
            "first_solve": stats.first_solve if stats.first_solve != default_datetime else 'jeszcze nie rozwiązana!'
        }
        puzzle_list.append(puzzle_entry)
    
    paginator = Paginator(puzzle_list, per_page=6)
    page_obj = paginator.get_page(page_num)
    
    context = {
        "page_obj": page_obj
        }
    return render(request, 'riddleme/page.html', context)

def puzzle(request, puzzle_id):
    puzzle = Puzzle.objects.get(pk=puzzle_id)
    solved = False
    
    if request.method == "POST":
        answer = request.POST['answer']
        answer = str.strip(answer).lower()
        
        if str.lower(puzzle.answer) == answer:
            solved = True
        
        date = localtime(timezone.now())
        
        Submitted.objects.create(
            uid=request.user, 
            pid=puzzle, 
            submitted=answer, 
            date=date, 
            correct=solved
        )
        
        if solved:
            messages.success(request, "Brawo, udało ci się rozwiązać zagadkę!")
            stat = PuzzleStatistics.objects.get(pid=puzzle)
            stat.first_solve = date
            stat.solved_count = stat.solved_count + 1
            stat.save()
        else:
            messages.warning(request, f"\"{answer}\" nie było poprawną odpowiedzią.")
        return redirect('puzzle', puzzle.id)
    
    subs = []
    if request.user.is_authenticated:
        submissions = Submitted.objects.filter(pid=puzzle, uid=request.user).order_by("-date")[:10]
    
        for sub in submissions:
            subs.append({
                "answer": sub.submitted,
                "date": sub.date,
                "correct": sub.correct
            })
            if sub.correct:
                solved = True
            
    
    context = {
        "puzzle_id": puzzle.id,
        "puzzle_title": puzzle.title,
        "puzzle_content": puzzle.content,
        "submissions": subs,
        "solved": solved
        }
    return render(request, 'riddleme/puzzle.html', context)

def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        
        submit_count = Submitted.objects.filter(uid=user).count()
        
        solved_count = Submitted.objects.filter(uid=user, correct=True) \
                                .order_by('pid').values('pid').distinct().count()
        
        puzzle_list = Submitted.objects.filter(uid=user, correct=True).order_by('-date').select_related('pid')
        plist = [{
            "puzzle_title":entry.pid.title,
            "puzzle_id": entry.pid.id,
            "date": entry.date,
            "sub_count": Submitted.objects.filter(uid=user, pid=entry.pid).count()
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
            return redirect('profile')
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