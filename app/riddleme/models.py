from datetime import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.db.models import signals


default_datetime = timezone.make_aware(datetime(year=1970, month=1, day=1))


# Create your models here.
class Puzzle(models.Model):
    title = models.TextField(verbose_name="Tytuł")
    content = models.TextField(verbose_name="Zawartość")
    answer = models.CharField(max_length=150, verbose_name="Odpowiedź")
    
    class Meta:
        verbose_name = "Zagadka"
        verbose_name_plural = "Zagadki"
    
class PuzzleStatistics(models.Model):
    pid = models.OneToOneField(Puzzle, on_delete=models.CASCADE, verbose_name="ID zagadki")
    solved_count = models.IntegerField(default=0, verbose_name="Liczba rozwiązań")
    first_solve = models.DateTimeField(verbose_name="Data pierwszego rozwiązania")
    
    class Meta:
        verbose_name = "Statystyki zagadek"
        verbose_name_plural = "Statystyki zagadek"
    
# signal method to create puzzle statistic that corresponds to new puzzle
def create_stats(sender, instance, created, **kwargs):
    if created:
        PuzzleStatistics.objects.create(pid = instance, 
                                        solved_count = 0, 
                                        first_solve = datetime(year=1970, month=1, day=1))
signals.post_save.connect(create_stats, sender=Puzzle, weak=False, dispatch_uid="riddleme.models.create_stats")
    
class Submitted(models.Model):
    pid = models.ForeignKey(Puzzle, on_delete=models.CASCADE, verbose_name="ID zagadki")
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="ID użytkownika")
    submitted = models.CharField(max_length=150, verbose_name="Zgłoszona odpowiedź")
    date = models.DateTimeField(verbose_name="Data zgłoszenia odpowiedzi")
    correct = models.BooleanField(verbose_name="Czy poprawna odpowiedź")
    
    class Meta:
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"