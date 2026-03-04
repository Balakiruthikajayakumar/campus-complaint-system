from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='lostfound_home'),
    path('add/', views.add_item, name='add_item'),
    path('claim/<int:id>/', views.claim_item, name='claim_item'),
    path('request-claim/<int:id>/', views.request_claim, name='request_claim'),
    path('approve-claim/<int:id>/', views.approve_claim, name='approve_claim'),

]