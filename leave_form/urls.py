from django.urls import path
from . import views

urlpatterns = [

    path("apply/", views.apply_leave, name="apply_leave"),

    path("download/<int:id>/", views.download_leave, name="download_leave"),

    path('leave_verification/', views.leave_verification, name='leave_verification'),

    path("tutor-approve/<int:id>/", views.tutor_approve),
path("tutor-reject/<int:id>/", views.tutor_reject),

]
