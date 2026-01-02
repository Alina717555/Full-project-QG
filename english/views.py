from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Lesson, Review, Enrollment, Payment
from .forms import ReviewForm

from django.db.models import Avg, Count


User = get_user_model()


def index(request):
    return render(request, 'english/index.html')


def catalog(request):
    search_query = request.GET.get('q', '').strip()
    lessons_queryset = Lesson.objects.all()

    if search_query:
        lessons_queryset = lessons_queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    enrolled_lessons = []
    if request.user.is_authenticated:
        enrolled_lessons = Lesson.objects.filter(enrollment__user=request.user)

    return render(request, 'english/catalog.html', {
        'lessons': lessons_queryset,
        'search_query': search_query,
        'enrolled_lessons': enrolled_lessons,
    })


def about(request):
    return render(request, 'english/about.html')



def feedback(request):
    review_form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('english:feedback')
        else:
            review_form = ReviewForm()

    approved_reviews = Review.objects.filter(is_approved=True)
    overall_avg = approved_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'english/feedback.html', {
        'approved_reviews': approved_reviews,
        'overall_avg': round(overall_avg, 1),
        'review_form': review_form
    })


def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)

    reviews = Review.objects.filter(lesson=lesson, is_approved=True)

    stats = reviews.aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )

    distribution_raw = reviews.values('rating').annotate(count=Count('rating'))

    distribution = {i: 0 for i in range(1, 6)}
    for item in distribution_raw:
        distribution[item['rating']] = item['count']

    total = stats['total_reviews'] or 1
    percents = {
        star: (count / total) * 100
        for star, count in distribution.items()
    }

    context = {
        'lesson': lesson,
        'reviews': reviews,
        'avg_rating': round(stats['avg_rating'] or 0, 1),
        'total_reviews': stats['total_reviews'],
        'distribution': distribution,
        'percents': percents,
    }

    return render(request, 'english/materials.html', context)



@login_required
def payment_page(request, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    return render(request, 'english/payment.html', {'lesson': lesson})

@login_required
def process_payment(request, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)

    if request.method == "POST":
        name = request.POST.get("name")
        card_number = request.POST.get("card_number")

        # Save payment
        Payment.objects.create(
            user=request.user,
            lesson=lesson,
            full_name=name,
            card_last4=card_number[-4:],
            amount=lesson.price,
            is_successful=True
        )

        Enrollment.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

        return redirect("english:courses")

    return redirect("english:payment_page", lesson_slug=lesson.slug)


@login_required
def courses(request):
    enrolled_lessons = Lesson.objects.filter(
        enrollment__user=request.user
    )
    all_lessons = Lesson.objects.all()

    return render(request, 'english/courses.html', {
        'enrolled_lessons': enrolled_lessons,
        'lessons': all_lessons,  
    })



@login_required
def course_material(request, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    return render(request, 'english/course material.html', {'lesson': lesson})


@login_required
def remove_course(request, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    Enrollment.objects.filter(user=request.user, lesson=lesson).delete()
    return redirect('english:courses')



def add_review(request, lesson_slug):
    if request.method == "POST" and request.user.is_authenticated:
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        Review.objects.create(
            lesson=lesson,
            user=request.user,
            rating=rating,
            comment=comment,
            is_approved=True
        )
       
        return redirect('english:lesson_detail', slug=lesson.slug) 
    
    return redirect('english:catalog') 


def feedback(request):
    all_lessons = Lesson.objects.all()
    selected_lesson_id = request.GET.get('course')
    all_reviews = Review.objects.filter(is_approved=True)
    if selected_lesson_id:
        all_reviews = all_reviews.filter(lesson_id=selected_lesson_id)

    stats = all_reviews.aggregate(
        avg_rating=Avg('rating'),
        total_count=Count('id')
    )
    
    distribution_raw = all_reviews.values('rating').annotate(count=Count('rating'))
    dist = {i: 0 for i in range(1, 6)}
    for entry in distribution_raw:
        dist[entry['rating']] = entry['count']
    
    total_reviews = stats['total_count'] or 1
    percents = {str(star): (count / total_reviews) * 100 for star, count in dist.items()}
    dist_str = {str(k): v for k, v in dist.items()}

    context = {
        'lessons': all_lessons,
        'reviews': all_reviews.order_by('-created_at'),
        'avg_rating': round(stats['avg_rating'] or 0, 1),
        'total_ratings': stats['total_count'],
        'dist': dist_str,
        'percents': percents,
        'selected_lesson': selected_lesson_id,
    }
    return render(request, 'english/feedback.html', context)