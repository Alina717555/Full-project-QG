from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    level = models.CharField(max_length=20, blank=True, null=True)

    def get_average_score(self):
        avg = QuizResult.objects.filter(user=self.user).aggregate(
            avg=Avg("score")
        )["avg"]
        return round(avg, 1) if avg else 0

    def get_completed_count(self):
        return QuizResult.objects.filter(user=self.user).count()

    def get_progress_percentage(self):
        avg = self.get_average_score()
        return max(0, min(100, int(avg)))

    def __str__(self):
        return self.user.username


class QuizResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quiz_results"
    )
    quiz_name = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    date_completed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_completed"]

    def __str__(self):
        return f"{self.quiz_name} – {self.score}% ({self.user.username})"

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=20, blank=True, null=True)
    lesson_date = models.DateTimeField(null=True, blank=True)  
