from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'english'

urlpatterns = [
    path('', views.index, name='index'),
    path('materials/<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('materials/<slug:lesson_slug>/add-review/', views.add_review, name='add_review'),
    path('payment/<slug:lesson_slug>/', views.payment_page, name='payment_page'),
    path('payment/<slug:lesson_slug>/process/', views.process_payment, name='process_payment'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('courses/', views.courses, name='courses'),
    path('courses/<slug:lesson_slug>/material/', views.course_material, name='course_material'),
    path('courses/remove/<slug:lesson_slug>/', views.remove_course, name='remove_course'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('feedback/', views.feedback, name='feedback'),

  
]
