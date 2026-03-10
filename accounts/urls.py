from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_user, name='register'),

    path('student/', views.student_home, name='student_homepage'),
    path('tutor/', views.tutor_home, name='tutor_homepage'),
    path('hod/', views.hod_home, name='hod_homepage'),
    path('principal/', views.principal_home, name='principal_homepage'),
    path("my-requests/", views.my_requests, name="my_requests"),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]