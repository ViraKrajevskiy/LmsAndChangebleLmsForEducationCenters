from django.urls import path
from MainApp.views.login_logout.login import login_view
from MainApp.views.login_logout.logout import logout_view
from MainApp.views.objects_views.view_see_profile import profile_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile')
]