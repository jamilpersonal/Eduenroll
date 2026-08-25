import json

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Course, Enrollment, Student, StudentTopicProgress, Topic


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'courses/login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    enrolled_course_ids = set(
        Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
    )

    all_courses = Course.objects.all()
    catalog = []
    for course in all_courses:
        catalog.append({
            'course': course,
            'is_enrolled': course.id in enrolled_course_ids,
        })

    my_courses = []
    for course in all_courses:
        if course.id in enrolled_course_ids:
            my_courses.append({
                'course': course,
                'progress': course.progress_percent_for(student),
            })

    context = {
        'student': student,
        'catalog': catalog,
        'my_courses': my_courses,
    }
    return render(request, 'courses/dashboard.html', context)


@login_required
@require_POST
def enroll_course(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(student=student, course=course)
    messages.success(request, f'You are now enrolled in {course.name}.')
    return redirect('dashboard')


@login_required
def course_detail(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    if not is_enrolled:
        messages.error(request, 'Enroll in this course to view its learning path.')
        return redirect('dashboard')

    completed_topic_ids = set(
        StudentTopicProgress.objects.filter(
            student=student, topic__module__course=course, is_completed=True
        ).values_list('topic_id', flat=True)
    )

    modules = course.modules.prefetch_related('topics').all()

    context = {
        'course': course,
        'modules': modules,
        'completed_topic_ids': completed_topic_ids,
        'progress': course.progress_percent_for(student),
        'total_topics': course.total_topics(),
        'completed_count': course.completed_topics_for(student),
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
@require_POST
def toggle_topic_complete(request, topic_id):
    """AJAX endpoint: toggles / sets a topic's completion state for the logged-in student."""
    student = get_object_or_404(Student, user=request.user)
    topic = get_object_or_404(Topic, id=topic_id)
    course = topic.module.course

    if not Enrollment.objects.filter(student=student, course=course).exists():
        return JsonResponse({'error': 'Not enrolled in this course.'}, status=403)

    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        payload = {}

    progress, _ = StudentTopicProgress.objects.get_or_create(student=student, topic=topic)

    if 'is_completed' in payload:
        progress.is_completed = bool(payload['is_completed'])
    else:
        progress.is_completed = not progress.is_completed
    progress.save()

    return JsonResponse({
        'topic_id': topic.id,
        'is_completed': progress.is_completed,
        'progress_percent': course.progress_percent_for(student),
        'completed_count': course.completed_topics_for(student),
        'total_topics': course.total_topics(),
    })
