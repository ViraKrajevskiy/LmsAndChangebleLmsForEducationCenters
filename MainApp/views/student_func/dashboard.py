from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
from MainApp.models import Lesson, NewsModels, StudentProfile


@login_required
def dashboard_view(request):
    user = request.user
    today = date.today()

    # 1. Получаем профиль студента
    student_profile = StudentProfile.objects.filter(user=user).select_related('group').first()

    # 2. ФИЛЬТР НОВОСТЕЙ
    # Показываем новости, где роль 'all' ИЛИ роль совпадает с ролью юзера ('student')
    news = NewsModels.objects.filter(
        Q(user_role='all') | Q(user_role=user.role)
    ).order_by('-date_field')[:3]

    # 3. ФИЛЬТР УРОКОВ
    lessons_data = []
    if student_profile and student_profile.group:
        current_lessons = Lesson.objects.filter(
            main__lesson_day=today,
            main__group=student_profile.group
        ).order_by('start_time')

        for lesson in current_lessons:
            lessons_data.append({
                'obj': lesson,
                'time_start': lesson.start_time.strftime('%H:%M'),
                'time_end': lesson.end_time.strftime('%H:%M'),
            })

    context = {
        'news': news,
        'lessons': lessons_data,
        'group': student_profile.group if student_profile else None,
        'today': today,
    }
    return render(request, 'student/dashboard.html', context)