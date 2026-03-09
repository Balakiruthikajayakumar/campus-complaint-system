from django.urls import path
from . import views


urlpatterns = [

    path('apply/',views.apply_outpass,name='apply_outpass'),

    path('list/',views.outpass_list,name='outpass_list'),

    path('approve/<int:id>/',views.approve_outpass,name='approve_outpass'),

    path('reject/<int:id>/',views.reject_outpass,name='reject_outpass'),

    path('my/' ,views.my_outpasses,name='my_outpass'),
    path('download/<int:id>/', views.download_outpass, name='download_outpass'),
]