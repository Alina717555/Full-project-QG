from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

class Lesson(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(default=3)
    age_range = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    content_html = models.TextField(verbose_name="Detailed Course Content")
    materials = models.JSONField(default=list, blank=True)
    ratings = models.JSONField(default=dict, blank=True) 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    
    @property
    def materials_with_colors(self):
        colors = ['white', 'purple']
        return [{'material': m, 'color': colors[i % 2]} for i, m in enumerate(self.materials)]

    def __str__(self):
        return self.title

class Review(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.lesson.title} - {self.user.username} - {self.rating} stars'

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.lesson.title}'
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    card_last4 = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} → {self.lesson} ({self.amount})"

