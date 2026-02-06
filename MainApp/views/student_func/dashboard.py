from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime
from MainApp.models import Lesson, NewsModels, StudentProfile, StudentGrade, HomeworkGrade


@login_required
def dashboard_view(request):
    user = request.user
    today = date.today()

    student_profile = StudentProfile.objects.filter(user=user).select_related('group').first()

    news = NewsModels.objects.filter(
        Q(user_role='all') | Q(user_role=user.role)
    ).order_by('-date_field')[:3]


    lessons_data = []
    if student_profile and student_profile.group:
        current_lessons = Lesson.objects.filter(
            main__lesson_day=today,
            main__group=student_profile.group
        ).order_by('start_time')

        for lesson in current_lessons:

            grade_obj = StudentGrade.objects.filter(student=student_profile, lesson=lesson).first()

            lessons_data.append({
                'obj': lesson,
                'time_start': lesson.start_time.strftime('%H:%M'),
                'time_end': lesson.end_time.strftime('%H:%M'),
                'grade': grade_obj.grade if grade_obj else None,
            })

    recent_marks = []
    if student_profile:

        l_grades = StudentGrade.objects.filter(student=student_profile).select_related('lesson__main')\
            .order_by('-id')[:3]
        for g in l_grades:
            recent_marks.append({
                'title': g.lesson.title,
                'grade': g.grade,
                'type': 'Урок',
                'date': g.lesson.main.lesson_day
            })


        h_grades = HomeworkGrade.objects.filter(student=student_profile).select_related('homework__lesson')\
            .order_by('-id')[:3]
        for h in h_grades:
            raw_date = h.homework.dedline
            if isinstance(raw_date, datetime):
                raw_date = raw_date.date()

            recent_marks.append({
                'title': h.homework.lesson.title,
                'grade': h.grade,
                'type': 'ДЗ',
                'date': raw_date
            })

    
    recent_marks = sorted(recent_marks, key=lambda x: x['date'], reverse=True)[:4]

    context = {
        'news': news,
        'lessons': lessons_data,
        'group': student_profile.group if student_profile else None,
        'today': today,
        'recent_marks': recent_marks,
    }
    return render(request, 'student/dashboard.html', context)