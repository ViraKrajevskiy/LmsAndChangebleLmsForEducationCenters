from django.urls import path
from MainApp.views.login_logout.login import login_view
from MainApp.views.login_logout.logout import logout_view
from MainApp.views.student_func.dashboard import dashboard_view
from MainApp.views.student_func.homework import homework_list_view
from MainApp.views.student_func.student_schedule import full_schedule_view
from MainApp.views.student_func.view_see_profile import profile_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('homework/', homework_list_view, name='homework'),
    path('schedule/', full_schedule_view, name='full_schedule')
]