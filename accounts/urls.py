from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('student/', views.student_home, name='student_homepage'),
    path('tutor/', views.tutor_home, name='tutor_homepage'),
    path('hod/', views.hod_home, name='hod_homepage'),
    path('principal/', views.principal_home, name='principal_homepage'),
    path('deputy-warden/', views.deputy_warden_home, name='deputy_warden_homepage'),
    path('associate-warden/', views.associate_warden_home, name='associate_warden_homepage'),
    path("my-requests/", views.my_requests, name="my_requests"),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('principal/complaints/', views.principal_complaints, name='principal_complaints'),
    path('approve/<int:id>/', views.approve_complaint, name='approve_complaint'),
    path('reject/<int:id>/', views.reject_complaint, name='reject_complaint'),
    path('principal/college/', views.principal_college_complaints, name='principal_college_complaints'),
path('principal/hostel/', views.principal_hostel_complaints, name='principal_hostel_complaints'),
path('principal/anonymous/', views.principal_anonymous_complaints, name='principal_anonymous_complaints'),
path('principal/college/', views.principal_college_complaints, name='principal_college_complaints'),

path('approve/<int:id>/', views.approve_complaint, name='approve_complaint'),
path('reject/<int:id>/', views.reject_complaint, name='reject_complaint'),
]