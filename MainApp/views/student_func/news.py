from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MainApp.models import NewsModels


@login_required
def news_list_view(request):
    user = request.user

    allowed_roles = ['all']

    if user.role == 'student':
        allowed_roles.append('student')
    elif user.role == 'teacher':
        allowed_roles.append('teacher')
    elif user.role == 'mentor':
        allowed_roles.append('mentor')
    news = NewsModels.objects.filter(
        user_role__in=allowed_roles
    ).order_by('-date_field')

    context = {
        'news': news,
    }
    return render(request, 'student/news_list.html', context)