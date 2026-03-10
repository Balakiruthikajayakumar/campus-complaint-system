from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # STUDENT
    # =====================================================

    # Submit Complaint
    path('submit/', views.submit_complaint, name='submit_complaint'),

    # Student view their own complaints
    path('my/', views.my_complaints, name='my_complaints'),



    # =====================================================
    # TUTOR DASHBOARD
    # =====================================================

    # Tutor complaint list
    path('tutor/', views.tutor_complaints, name='tutor_complaints'),

    # Tutor approve complaint
    path('approve/<int:id>/', views.approve_by_tutor, name='approve_tutor'),

    # Tutor reject complaint
    path('reject/<int:id>/', views.reject_by_tutor, name='reject_tutor'),


    # =====================================================
    # HOD DASHBOARD
    # =====================================================
    #HOD HOME PAGE
    path("hod/", views.hod_homepage, name="hod_homepage"),
    # HOD complaint list
    path('hod/', views.hod_complaints, name='hod_complaints'),

    # HOD approve complaint
    path('hod/approve/<int:id>/', views.approve_by_hod, name='approve_hod'),

    # HOD reject complaint
    path('hod/reject/<int:id>/', views.reject_by_hod, name='reject_hod'),

    path("hod/profile/", views.hod_profile, name="hod_profile"),


    # =====================================================
    # PRINCIPAL DASHBOARD
    # =====================================================

    # Principal complaint list
    path('principal/', views.principal_complaints, name='principal_complaints'),

    # Principal approve (resolve complaint)
    path('principal/approve/<int:id>/', views.approve_by_principal, name='approve_principal'),

    # Principal reject complaint
    path('principal/reject/<int:id>/', views.reject_by_principal, name='reject_principal'),


    # =====================================================
    # ANONYMOUS COMPLAINT
    # =====================================================

    # Anonymous complaint submission
    path('anonymous/', views.anonymous_complaint, name='anonymous_complaint'),
    
    #Track complaint
    path('track/<int:id>/', views.track_complaint, name='track_complaint'),
    path("complaints/", views.complaints_page, name="complaints"),

    path("view/<int:id>/", views.view_complaint, name="view_complaint"),
    path("tutor/profile/", views.tutor_profile, name="tutor_profile"),
]
