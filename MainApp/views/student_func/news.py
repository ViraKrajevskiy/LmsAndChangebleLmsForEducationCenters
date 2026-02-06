from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from MainApp.models import NewsModels


@login_required
def news_list_view(request):
    user = request.user

    # Базовый список: то, что видят все
    allowed_roles = ['all']

    # Добавляем специфические роли в зависимости от того, кто авторизован
    if user.role == 'student':
        allowed_roles.append('student')
    elif user.role == 'teacher':
        allowed_roles.append('teacher')
    elif user.role == 'mentor':
        allowed_roles.append('mentor')

    # Фильтруем новости: только те, что входят в наш список разрешенных
    news = NewsModels.objects.filter(
        user_role__in=allowed_roles
    ).order_by('-date_field')

    context = {
        'news': news,
    }
    return render(request, 'student/news_list.html', context)