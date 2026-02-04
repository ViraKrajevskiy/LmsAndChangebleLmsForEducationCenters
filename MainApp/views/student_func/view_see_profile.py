from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MainApp.models import StudentProfile, MentorProfile, TeacherProfile

@login_required
def profile_view(request):
    user = request.user

    student = None
    mentor = None
    teacher = None

    if user.role == 'student':
        student = StudentProfile.objects.filter(user=user).first()
    elif user.role == 'mentor':
        mentor = MentorProfile.objects.filter(user=user).first()
    elif user.role == 'teacher':
        teacher = TeacherProfile.objects.filter(user=user).first()

    return render(request, "profile/profile.html", {
        "user": user,
        "student": student,
        "mentor": mentor,
        "teacher": teacher,
    })
