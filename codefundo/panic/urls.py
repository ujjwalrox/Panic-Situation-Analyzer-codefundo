from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.map, name='map'),
    path('signup/', views.SignUp, name='SignUp'),
    path('locations/', views.locations, name='locations'),
    path('api/location/', views.api_location, name="api_l"),
    path('api/paniclocation/', views.api_panic_location, name="api_pl"),
    path('mapalgo/', views.map_algo, name='map_algo'),
]
