from django.urls import path
from . import views

urlpatterns = [

    path("apply/", views.apply_leave, name="apply_leave"),

    path("my/", views.my_requests, name="leave_my_requests"),

    path("download/<int:id>/", views.download_leave, name="download_leave"),

    path("tutor/", views.leave_verification, name="leave_verification"),
    path("tutor/approve/<int:id>/", views.tutor_approve, name="tutor_approve"),
    path("tutor/reject/<int:id>/", views.tutor_reject, name="tutor_reject"),

    path("hod/", views.hod_leave_page, name="hod_leave_page"),
    path("hod/approve/<int:id>/", views.hod_approve, name="hod_approve"),

    path("deputy/", views.deputy_leave_page, name="deputy_leave_page"),
    path("deputy/approve/<int:id>/", views.deputy_approve, name="deputy_approve"),

    path("warden/", views.warden_leave_page, name="warden_leave_page"),
    path("warden/approve/<int:id>/", views.final_approve, name="final_approve"),

]