from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
# Register your models here.

@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
@admin.register(PuzzleStatistics)
class PuzzleStatisticsAdmin(admin.ModelAdmin):
    list_display = ("id", "view_puzzle_link")
    
    @admin.display(description="Zagadka")
    def view_puzzle_link(self, obj):
        url = (
            reverse("admin:riddleme_puzzle_changelist")
        )
        return format_html('<a href="{}">{}</a>', url, obj.pid)
@admin.register(Submitted)
class SubmittedAdmin(admin.ModelAdmin):
    list_display = ("id", "view_puzzle_link", "view_user_link", "submitted", "correct")
    
    @admin.display(description="Zagadka")
    def view_puzzle_link(self, obj):
        url = (
            reverse("admin:riddleme_puzzle_changelist")
        )
        return format_html('<a href="{}">{}</a>', url, obj.pid)
    
    @admin.display(description="Użytkownik")
    def view_user_link(self, obj):
        url = (
            reverse("admin:auth_user_changelist")
        )
        return format_html('<a href="{}">{}</a>', url, obj.uid)