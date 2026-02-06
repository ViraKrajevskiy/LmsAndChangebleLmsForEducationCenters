from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MainApp.models import StudentProfile, HomeWork, HomeworkSubmission, HomeworkGrade


@login_required
def homework_list_view(request):
    student_profile = StudentProfile.objects.filter(user=request.user).first()

    if not student_profile:
        return render(request, "student/homework.html", {"no_profile": True})

    # Получаем все задания для группы студента
    homeworks = HomeWork.objects.filter(
        lesson__main__group=student_profile.group
    ).order_by('dedline')

    hw_list = []
    for hw in homeworks:
        # 1. Ищем факт сдачи работы
        submission = HomeworkSubmission.objects.filter(
            student=student_profile,
            homework=hw
        ).first()

        # 2. Ищем оценку (исправлено: ищем по homework и student, как просит Django)
        grade = HomeworkGrade.objects.filter(
            homework=hw,
            student=student_profile
        ).first()

        hw_list.append({
            'info': hw,
            'submission': submission,
            'grade': grade,
        })

    return render(request, "student/homework.html", {
        "homeworks": hw_list,
        "group": student_profile.group
    })