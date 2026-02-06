from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MainApp.models import StudentGrade, HomeworkGrade, StudentAbsentOrCame

@login_required
def full_grade_report_view(request):
    user = request.user
    # 1. Оценки за уроки (активность)
    lesson_grades = StudentGrade.objects.filter(student__user=user).select_related('lesson')

    # 2. Оценки за домашку
    homework_grades = HomeworkGrade.objects.filter(student__user=user).select_related('homework')

    # 3. Посещаемость (чтобы видеть 'н-ки' в этой же таблице)
    attendance = StudentAbsentOrCame.objects.filter(student__user=user).select_related('lesson')

    report_data = []

    for g in lesson_grades:
        report_data.append({
            # Если это DateTimeField, добавляем .date()
            'date': g.lesson.main.lesson_day,
            'subject': g.lesson.title,
            'type': 'Урок',
            'grade': g.grade,
            'status': 'Present',
            'comment': g.comment
        })

    for h in homework_grades:
        # ИСПРАВЛЕНИЕ: принудительно берем только дату, если там datetime
        h_date = h.homework.dedline
        if hasattr(h_date, 'date'):
            h_date = h_date.date()

        report_data.append({
            'date': h_date,
            'subject': h.homework.lesson.title,
            'type': 'Домашняя работа',
            'grade': h.grade,
            'status': 'Present',
            'comment': h.comment
        })

    for a in attendance:
        if a.status != 'Present':
            report_data.append({
                'date': a.lesson.main.lesson_day,
                'subject': a.lesson.title,
                'type': 'Посещаемость',
                'grade': '—',
                'status': a.status,
                'comment': a.comment or a.get_status_display()
            })

    # Теперь все объекты в 'date' — это datetime.date, и сортировка сработает
    report_data.sort(key=lambda x: x['date'], reverse=True)

    return render(request, 'student/full_report.html', {'report': report_data})
