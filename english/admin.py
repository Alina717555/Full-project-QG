from django.contrib import admin

from .models import Payment, Review

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "amount", "is_successful", "created_at")
    list_filter = ("is_successful", "created_at")



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'lesson')
    search_fields = ('user__username', 'comment')
