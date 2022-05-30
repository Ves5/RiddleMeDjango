from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Puzzle)
admin.site.register(PuzzleStatistics)
admin.site.register(Submitted)