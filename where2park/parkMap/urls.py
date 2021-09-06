
from django.urls import path

from . import views

urlpatterns = [
    # path('test', views.test, name = 'test'),
    # path('test/<str:lat>/<str:lon>/<str:threshold>', views.getNearestMeters, name = 'getMeters'), # e.g.: http://localhost:8000/parkmap/distance/49.2827/-123.1207/10
    path('', views.index, name='index'),
    path('<str:meter_id>/', views.detail, name='detail'),
    path('<str:meter_id>/rate', views.getMeterRate, name = 'getRate'),
    path('distance/<str:lat>/<str:lon>/<str:threshold>', views.getNearestMeters, name = 'getMeters'), # e.g.: http://localhost:8000/parkmap/distance/49.2827/-123.1207/10
    path('update-marker/<str:lat>/<str:lon>/<str:threshold>', views.getNearestMetersJSON, name = 'updateMarker'),
]