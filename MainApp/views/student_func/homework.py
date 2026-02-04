from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MainApp.models import StudentProfile, HomeWork, HomeworkSubmission

@login_required
def homework_list_view(request):
    user = request.user
    # Безопасно получаем профиль
    student_profile = StudentProfile.objects.filter(user=user).first()

    if not student_profile:
        return render(request, "student/homework.html", {"no_profile": True})

    homeworks = HomeWork.objects.filter(lesson__main__group=student_profile.group).order_by('dedline')
    # Собираем данные: было ли сдано задание и какая оценка
    hw_list = []
    for hw in homeworks:
        submission = HomeworkSubmission.objects.filter(student=student_profile, homework=hw).first()
        hw_list.append({
            'info': hw,
            'submission': submission,
        })

    return render(request, "student/homework.html", {
        "homeworks": hw_list,
        "group": student_profile.group
    })