from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import UserProfile, QuizResult



class QuizResultInline(admin.TabularInline):
    model = QuizResult
    fk_name = "user"
    extra = 0
    readonly_fields = ("date_completed",)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fields = ("gender", "dob", "level", "avatar")
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, QuizResultInline)

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    ordering = ("username",)



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "gender", "level", "avatar_preview")
    readonly_fields = ("avatar_preview",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;" />',
                obj.avatar.url
            )
        return "No image"



@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz_name", "score", "date_completed")
    list_filter = ("quiz_name", "user")
    search_fields = ("quiz_name", "user__username")
