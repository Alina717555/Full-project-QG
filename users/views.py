from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import json
from collections import defaultdict

from .forms import UserRegistrationForm
from .models import UserProfile, QuizResult, Lesson  
from english.models import Enrollment  
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('english:index')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/registrationn.html', {
        'form': form,
        'title': 'Register'
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'english:index')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/signup.html', {'form': form, 'title': 'Sign In'})



def logout_view(request):
    logout(request)
    return redirect('english:index')






@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    recent_quizzes = QuizResult.objects.filter(user=user)[:3]

    today = timezone.now().date()
    today_lessons = Lesson.objects.filter(lesson_date__date=today).order_by('lesson_date')

    test1 = QuizResult.objects.filter(user=user, quiz_name__icontains="test1").first()

    lessons = Lesson.objects.annotate(
        year=ExtractYear('lesson_date'),
        month=ExtractMonth('lesson_date'),
        day=ExtractDay('lesson_date')
    ).values('id','title','year','month','day','lesson_date')

    lessons_by_date = defaultdict(list)
    for l in lessons:
        date_str = f"{l['year']}-{l['month']:02d}-{l['day']:02d}"
        lessons_by_date[date_str].append({'id': l['id'], 'title': l['title']})

    context = {
        'profile': profile,
        'recent_quizzes': recent_quizzes,
        'today_lessons': today_lessons,
        'test1_score': test1.score if test1 else 0,
        'lessons_by_date': dict(lessons_by_date),
    }
    return render(request, 'users/ui.html', context)



@login_required
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.avatar = request.FILES['avatar']
        profile.save()
        return JsonResponse({'status': 'success', 'url': profile.avatar.url})
    return JsonResponse({'status': 'error'}, status=400)



@login_required
def update_profile_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            profile_obj, _ = UserProfile.objects.get_or_create(user=user)

            user.first_name = data.get('name', user.first_name)
            user.save()

            profile_obj.gender = data.get('gender', profile_obj.gender)
            profile_obj.dob = data.get('dob') if data.get('dob') else profile_obj.dob
            profile_obj.level = data.get('level', profile_obj.level)
            profile_obj.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)



@login_required
def ui_elements(request):
    return profile(request)




