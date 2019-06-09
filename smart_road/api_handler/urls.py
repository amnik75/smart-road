from django.urls import path, include

urlpatterns = [
    path('location/', include('main.api.urls')),
    path('speed/', include('main.api.urls')),
    path('camera/', include('main.api.urls')),
]
