from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MainApp.models import StudentProfile, LessonMain

@login_required
def full_schedule_view(request):
    user = request.user
    student_profile = StudentProfile.objects.filter(user=user).first()


    schedule_days = LessonMain.objects.filter(
        group=student_profile.group
    ).order_by('lesson_day').prefetch_related('lessons')

    return render(request, 'student/student_schedule/../../templates/student/full_schedule.html', {
        'schedule_days': schedule_days,
        'group': student_profile.group
    })