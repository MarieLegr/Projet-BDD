from django.urls import path
from . import views

urlpatterns = [
    path('index1', views.index1, name='index1'),
    path('index', views.index, name='index'),
    path('autre_page', views.vue2, name='vue2'),
    path('Employee', views.vue3, name='vue3'),
    path('', views.index1, name='vide'), #REMPLACER index1 PAR index
    path('search_employee', views.search_employee, name='search_employee'),
    path('vue5', views.vue5, name='vue5'),
    path('test', views.vue4, name='vue4'),
    path('vue6', views.vue6, name='vue6'),
    path('search_employee3', views.search_employee3, name='search_employee3'),
    path('request4', views.request4, name='request4'),
    path('couples_employes', views.couples_employes, name='couples_employes'),
    path('requete1', views.requete1, name='requete1'),
    path('attributs_employes', views.attributs_employes, name='attributs_employes'),
    path('requete2', views.requete2, name='requete2'),
    path('employeXmail', views.employeXmail , name='employeXmail'),
    path('requete3', views.requete3, name='requete3'),
    path('List_comu_empl', views.List_comu_empl, name='List_comu_empl'),
    path('requete5', views.requete5, name='requete5'),
    path('PgdNBmail', views.PgdNBmail, name='PgdNBmail'),
    path('requete6', views.requete6, name='requete6'),
    path('listemots', views.listemots, name='listemots'),

]
