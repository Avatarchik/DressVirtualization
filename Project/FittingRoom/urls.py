from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'FittingRoom-Home'),
    path('home/', views.home, name = 'FittingRoom-Home'),
    path('our_model/', views.display_model, name = 'FittingRoom-Model'),
    path('contact/', views.contact, name = 'FittingRoom-Contact'),
    path('dress_list/', views.dress_library, name = 'FittingRoom-Dress-Library'),
]
