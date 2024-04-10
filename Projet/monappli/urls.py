from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('autre_page', views.vue2, name='vue2'),
    path('Employee', views.vue3, name='vue3'),
    path('', views.index, name='vide')
]
