from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.index, name='vide'), #REMPLACER index1 PAR index
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
    path('Liste_mots', views.Liste_mots, name='Liste_mots'),
    path('mail/<int:mail_id>/', views.detail_mail, name='detail_mail'),
    path('requete7', views.requete7, name='requete7'),
    path('conv', views.conv, name='conv'),

]
