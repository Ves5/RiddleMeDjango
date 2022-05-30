from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'riddleme/index.html')

def page(request, page_num):
    return HttpResponse(f"You're on page {page_num}")

def puzzle(request, puzzle_id):
    return HttpResponse(f"You're accessing puzzle {puzzle_id}")

def profile(request):
    return HttpResponse("Your profile page")

def login(request):
    return HttpResponse("Login page")

def logout(request):
    return redirect('index')

def register(request):
    return HttpResponse("Register page")