# MainApp/views/profile_views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from MainApp.models.Students.Model_student import StudentProfile
from MainApp.models.Workers.mentor_model import MentorProfile
from MainApp.models.Workers.teacher_model import TeacherProfile
from MainApp.models.roles.models_roles import User


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
