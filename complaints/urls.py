from django.urls import path
from . import views

urlpatterns = [

    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('my/', views.my_complaints, name='my_complaints'),

    # Tutor
    path('tutor/', views.tutor_complaints, name='tutor_complaints'),
    path('approve/<int:id>/', views.approve_by_tutor, name='approve_tutor'),
    path('reject/<int:id>/', views.reject_by_tutor, name='reject_tutor'),

    # HOD
    path('hod/', views.hod_complaints, name='hod_complaints'),
    path('hod/approve/<int:id>/', views.approve_by_hod, name='approve_hod'),
    path('hod/reject/<int:id>/', views.reject_by_hod, name='reject_hod'),

    # Principal ✅ FIXED
    path('principal/', views.principal_complaints, name='principal_complaints'),
    path('principal/approve/<int:id>/', views.approve_by_principal, name='approve_principal'),
    path('principal/reject/<int:id>/', views.reject_by_principal, name='reject_principal'),
]