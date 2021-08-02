
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:meter_id>/', views.detail, name='detail'),
    path('<str:meter_id>/rate', views.getMeterRate, name = 'getRate'),
    path('distance/<str:lat>/<str:lon>/<str:threshold>', views.getClosestMeters, name = 'getMeters')
]