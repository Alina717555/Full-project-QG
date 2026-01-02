from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('profile/', views.profile, name='profile'),
    path('upload-avatar/', views.upload_avatar, name='upload_avatar'),
    path('update-profile-ajax/', views.update_profile_ajax, name='update_profile_ajax'),
    path('ui/', views.ui_elements, name='ui'),
]