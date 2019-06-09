from django.urls import path, include
from main.api import views

urlpatterns = [
    path('getCuLocation/', views.GetCuLocation.as_view()),
    path('getLocations/', views.GetLocations.as_view()),
    path('getNumCar/', views.GetNumCar.as_view()),
    path('getSpeedCar/', views.GetSpeedCar.as_view()),
    path('createCamera/', views.CreateCamera.as_view()),
    path('updateCamera/', views.UpdateCamera.as_view()),
    path('createRoad/', views.CreateRoad.as_view()),
]
