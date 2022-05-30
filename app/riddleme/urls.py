from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:page_num>/', views.page, name='page'),
    path('puzzle/<int:puzzle_id>/', views.puzzle, name='puzzle'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register', views.register, name='register')
]