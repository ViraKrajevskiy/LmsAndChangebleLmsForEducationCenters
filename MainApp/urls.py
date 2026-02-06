from django.urls import path
from MainApp.views.login_logout.login import login_view
from MainApp.views.login_logout.logout import logout_view
from MainApp.views.student_func.dashboard import dashboard_view
from MainApp.views.student_func.grade import full_grade_report_view
from MainApp.views.student_func.homework import homework_list_view
from MainApp.views.student_func.news import news_list_view
from MainApp.views.student_func.student_schedule import full_schedule_view, lesson_detail_view
from MainApp.views.student_func.view_see_profile import profile_view
from MainApp.views.student_func.hw_detail import homework_detail

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', profile_view, name='profile'),

    path('news/', news_list_view, name='all_news'),
    
    path('homework/', homework_list_view, name='homework'),
    path('homework/<int:pk>/', homework_detail, name='homework_detail'),

    path('schedule/', full_schedule_view, name='full_schedule'),
    path('lesson/<int:pk>/', lesson_detail_view, name='lesson_detail'),

    path('grades/', full_grade_report_view, name='grade_statistics'),
]