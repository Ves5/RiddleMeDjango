from django.db import models
from django.conf import settings

# Create your models here.
class Puzzle(models.Model):
    title = models.TextField()
    content = models.TextField()
    answer = models.CharField(max_length=150)
    
class PuzzleStatistics(models.Model):
    pid = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    solved_count = models.IntegerField(default=0)
    first_solve = models.DateTimeField('date of first correct answer')
    
class Submitted(models.Model):
    pid = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted = models.CharField(max_length=150)
    date = models.DateTimeField('time of answer submission')
    correct = models.BooleanField()