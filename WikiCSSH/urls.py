from django.urls import path, include
from WikiCSSH import views
urlpatterns = [
    path('',views.home),
    path('tapping',views.tapping),
    path('visualize',views.visualize)
]