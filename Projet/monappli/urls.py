from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('autre_page', views.vue2, name='vue2'),
    path('Employee', views.vue3, name='vue3'),
    path('', views.index, name='vide'),
    path('search_employee', views.search_employee, name='search_employee'),
    path('vue5', views.vue5, name='vue5'),
    path('test', views.vue4, name='vue4'),
    path('vue6', views.vue6, name='vue6'),
    path('search_employee3', views.search_employee3, name='search_employee3'),

]
