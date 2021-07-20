from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('travels', views.travels),
    path('travels/add', views.addtrip),
    path('travels/destination/<int:id>', views.destination),
    path('logout', views.logout),
]

