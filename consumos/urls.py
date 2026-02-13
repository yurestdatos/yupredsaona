
from django.urls import path
from .views import tabla_consumos

urlpatterns = [
    path("", tabla_consumos, name="tabla_consumos"),
]
