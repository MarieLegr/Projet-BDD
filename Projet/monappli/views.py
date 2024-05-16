from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from .models import Category
from .models import Mail
from .models import AdresseMail
from .models import Receiver
from django.db import connection
import pandas as pd
import plotly
import plotly.express as px
from itertools import product
import plotly.graph_objects as go




def index(request):
    return render(request, "index.tmpl")

# Create your views here.
def index1(request):
    employees=Employee.objects.all()
    #category=Category.objects.all()
    context={"employees":employees}
    return render(request,"index1.tmpl",context=context)


#couples d’employés ayant communiqué dans un intervalle de temps choisi (liste
#ordonnée suivant le nombre de mails échangés, tronquée au-dessous d’un seuil
#paramétrable) ;



def request4(request):
    return render(request, 'requete4.tmpl',
                  {

                  })


def couples_employes(request):
    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        seuil = request.POST.get('seuil')

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
    CASE WHEN e.prenom < f.prenom OR (e.prenom = f.prenom AND e.nom < f.nom) THEN e.prenom ELSE f.prenom END AS prenom_employe1,
    CASE WHEN e.prenom < f.prenom OR (e.prenom = f.prenom AND e.nom < f.nom) THEN e.nom ELSE f.nom END AS nom_employe1,
    CASE WHEN e.prenom < f.prenom OR (e.prenom = f.prenom AND e.nom < f.nom) THEN f.prenom ELSE e.prenom END AS prenom_employe2,
    CASE WHEN e.prenom < f.prenom OR (e.prenom = f.prenom AND e.nom < f.nom) THEN f.nom ELSE e.nom END AS nom_employe2,
    COUNT(*) AS total_mails_echanges
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
INNER JOIN monappli_adressemail a ON m.sender_id = a.id
INNER JOIN monappli_adressemail b ON r.receiver_id = b.id
INNER JOIN monappli_employee e ON a.employee_id_id = e.id
INNER JOIN monappli_employee f ON b.employee_id_id = f.id
WHERE date BETWEEN %s AND %s and r.type_r != 'Bcc'
GROUP BY prenom_employe1, nom_employe1, prenom_employe2, nom_employe2
HAVING COUNT(*) > %s
ORDER BY COUNT(*) DESC;
            """, [date_debut, date_fin, seuil])
            rows = cursor.fetchall()

        couples = []
        for row in rows:
            nom1, prenom1, nom2, prenom2, nb_mails = row
            couples.append({
                'nom1': nom1,
                'prenom1': prenom1,
                'nom2': nom2,
                'prenom2': prenom2,
                'nb_mails': nb_mails
            })

        context = {
            'couples': couples,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'seuil': seuil
        }
        return render(request, 'couples_employes.tmpl', context)



def requete1(request):
    employees = Employee.objects.all()
    context = {"employees": employees}
    return render(request, "requete1.tmpl", context=context)

def attributs_employes(request):
    if request.method == 'POST':
        id = request.POST.get('employe')
        employe = Employee.objects.get(id=id)
        employe_nom = employe.nom
        employe_prenom = employe.prenom
        adresse_employe = request.POST.get('adresse_employe')

        if adresse_employe == "":
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.nom, e.prenom, c.name, am.adressemail
                    FROM monappli_employee e
                    LEFT JOIN monappli_category c ON e.category_id_id = c.id
                    LEFT JOIN monappli_adressemail am ON e.id = am.employee_id_id
                    WHERE e.nom = %s AND e.prenom = %s;
                """, [employe_nom, employe_prenom,])
                rows = cursor.fetchall()

            if rows:
                coupleadress=[]
                for row in rows:
                    nom_employe, prenom_employe, categorie, adresse_employe = row
                    coupleadress.append(adresse_employe)


                if not categorie:
                    categorie = "Aucune catégorie trouvée."

            context = {
                'nom_employe': nom_employe,
                'prenom_employe': prenom_employe,
                'categorie': categorie,
                'coupleadress': coupleadress
                }
            return render(request, 'attributs_employes.tmpl', context)


        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.nom, e.prenom, c.name, am.adressemail 
                    FROM monappli_employee e
                    LEFT JOIN monappli_category c ON e.category_id_id = c.id
                    LEFT JOIN monappli_adressemail am ON e.id = am.employee_id_id
                    WHERE e.id IN (SELECT employee_id_id FROM monappli_adressemail WHERE adressemail = %s);
                """, [adresse_employe])
                rows = cursor.fetchall()

            if rows:
                coupleadress=[]
                for row in rows:
                    nom_employe, prenom_employe, categorie, adresse_employe = row
                    coupleadress.append(adresse_employe)

                    if not categorie:
                        categorie = "Aucune catégorie trouvée."

            else:
                coupleadress = []
                categorie = "Aucune catégorie trouvée."



            context = {
                'nom_employe': nom_employe,
                'prenom_employe': prenom_employe,
                'categorie': categorie,
                'coupleadress': coupleadress
            }

            return render(request, 'attributs_employes.tmpl', context)
    else:
        return render(request, 'requete1.tmpl')
  

def requete2(request):
    return render(request, 'requete2.tmpl',
                  {

                  })


def employeXmail(request):
    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        seuil = request.POST.get('seuil')

        if seuil == "" or int(seuil) < 0:
            return render(request, 'requete2.tmpl',{
            })


        with connection.cursor() as cursor:
            cursor.execute("""SELECT
     e.nom, e.prenom , COUNT(*) AS nombre_de_mails_envoyes
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
inner join monappli_employee e on a.employee_id_id = e.id
WHERE m.date BETWEEN %s AND %s AND b.intext = true AND r.type_r != 'Bcc'
GROUP BY e.nom, e.prenom
having count(*) > %s;""", [date_debut, date_fin, seuil])

            rows1 = cursor.fetchall()


            liste1=[]
            for row in rows1:
                nom, prenom, nb_mails_envoyes = row
                liste1.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_envoyes': nb_mails_envoyes
                })

            liste1 = sorted(liste1, key=lambda x: x['nb_mails_envoyes'], reverse=True)
            liste11 = liste1[:10]

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
     e.nom, e.prenom , COUNT(*) AS nombre_de_mails_envoyes
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
inner join monappli_employee e on a.employee_id_id = e.id
WHERE m.date BETWEEN %s AND %s AND b.intext = false AND r.type_r != 'Bcc'
GROUP BY e.nom, e.prenom
having count(*) > %s;""", [date_debut, date_fin, seuil])

            rows11 = cursor.fetchall()
            liste5 = []
            for row in rows11:
                nom, prenom, nb_mails_envoyes = row
                liste5.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_envoyes': nb_mails_envoyes
                })

            liste5 = sorted(liste5, key=lambda x: x['nb_mails_envoyes'], reverse=True)
            liste55 = liste5[:10]


            if len(liste11) > 0 and len(liste55) > 0:


                DF1 = pd.DataFrame(liste11)
                DF2 = pd.DataFrame(liste55)

                trace1 = go.Bar(x=DF1['nom'], y=DF1['nb_mails_envoyes'], marker=dict(color='rgb(242, 65, 65)'),
                                name='Inerne')
                trace2 = go.Bar(x=DF2['nom'], y=DF2['nb_mails_envoyes'], marker=dict(color='rgb(47, 118, 128)'),
                                name='Externe')

                # Création de la figure avec les deux traces
                fig = go.Figure(data=[trace1, trace2])

                fig.update_layout(title=f'Principaux employés ayant envoyé plus de {seuil} mails', xaxis_title='Employés',
                                  yaxis_title='Nombre de mails envoyés', width=600, height=400, barmode='group', legend=dict(
                        x=1.0,
                        y=1.0,
                        bgcolor='rgba(255, 255, 255, 0)',
                        bordercolor='rgba(255, 255, 255, 0)'
                    ), showlegend=True)

                disp1 = plotly.offline.plot(fig, output_type='div')

            else:
                disp1 = []

        with connection.cursor() as cursor:
            cursor.execute("""SELECT t.nom, t.prenom, SUM(recus.nb_mails_recus) AS total_mails_recus
FROM (
    SELECT e.nom, e.prenom, a.id
    FROM monappli_employee e
    INNER JOIN monappli_adressemail a ON e.id = a.employee_id_id
) AS t
INNER JOIN (
    SELECT r.receiver_id, COUNT(*) AS nb_mails_recus
    FROM monappli_receiver r
    INNER JOIN monappli_mail m ON r.mail_id_id = m.id
    INNER JOIN monappli_adressemail a ON m.sender_id = a.id
    WHERE m.date BETWEEN %s AND %s AND r.type_r != 'Bcc' and a.intext = true
    GROUP BY r.receiver_id
    HAVING COUNT(*) > %s
) AS recus ON recus.receiver_id = t.id
GROUP BY t.nom, t.prenom;""", [date_debut, date_fin, seuil])
            rows2 = cursor.fetchall()

            liste2 = []
            for row in rows2:
                nom, prenom, nb_mails_recu = row
                liste2.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_recu': nb_mails_recu
                })

                # trier par odre decroissant
            liste2 = sorted(liste2, key=lambda x: x['nb_mails_recu'], reverse=True)
            liste22 = liste2[:10]


            with connection.cursor() as cursor:
                cursor.execute("""SELECT t.nom, t.prenom, SUM(recus.nb_mails_recus) AS total_mails_recus
FROM (
    SELECT e.nom, e.prenom, a.id
    FROM monappli_employee e
    INNER JOIN monappli_adressemail a ON e.id = a.employee_id_id
) AS t
INNER JOIN (
    SELECT r.receiver_id, COUNT(*) AS nb_mails_recus
    FROM monappli_receiver r
    INNER JOIN monappli_mail m ON r.mail_id_id = m.id
    INNER JOIN monappli_adressemail a ON m.sender_id = a.id
    WHERE m.date BETWEEN %s AND %s AND r.type_r != 'Bcc' and a.intext = false
    GROUP BY r.receiver_id
    HAVING COUNT(*) > %s
) AS recus ON recus.receiver_id = t.id
GROUP BY t.nom, t.prenom;""", [date_debut, date_fin, seuil])
                rows22 = cursor.fetchall()

                liste6 = []
                for row in rows22:
                    nom, prenom, nb_mails_recu = row
                    liste6.append({
                        'nom': nom,
                        'prenom': prenom,
                        'nb_mails_recu': nb_mails_recu
                    })

                # trier par odre decroissant
                liste6 = sorted(liste6, key=lambda x: x['nb_mails_recu'], reverse=True)
                liste66 = liste6[:10]

                if len(liste66) > 0 and len(liste22) > 0:

                    DF1= pd.DataFrame(liste22)
                    DF2= pd.DataFrame(liste66)
                    trace1 = go.Bar(x=DF1['nom'], y=DF1['nb_mails_recu'], marker=dict(color='rgb(242, 65, 65)'),
                                    name='Inerne')
                    trace2 = go.Bar(x=DF2['nom'], y=DF2['nb_mails_recu'], marker=dict(color='rgb(47, 118, 128)'),
                                    name='Externe')
                    fig = go.Figure(data=[trace1, trace2])
                    fig.update_layout(title=f'Principaux employés ayant reçu plus de {seuil} mails',xaxis_title='Employés',yaxis_title='Nombre de mails reçus',width=600, height=400)
                    disp2=plotly.offline.plot(fig,output_type='div')

                else:
                    disp2 = []





        with connection.cursor() as cursor:
            cursor.execute("""SELECT
     e.nom, e.prenom , COUNT(*) AS nombre_de_mails_envoyes
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
inner join monappli_employee e on a.employee_id_id = e.id
WHERE m.date BETWEEN %s AND %s AND b.intext = true AND r.type_r != 'Bcc'
GROUP BY e.nom, e.prenom
having count(*) < %s;""", [date_debut, date_fin, seuil])
            rows3 = cursor.fetchall()

            liste3=[]
            for row in rows3:
                nom, prenom, nb_mails_envoyes = row
                liste3.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_envoyes': nb_mails_envoyes
                })
            liste3 = sorted(liste3, key=lambda x: x['nb_mails_envoyes'], reverse=True)
            liste33 = liste3[:10]


        with connection.cursor() as cursor:
            cursor.execute("""SELECT
     e.nom, e.prenom , COUNT(*) AS nombre_de_mails_envoyes
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
inner join monappli_employee e on a.employee_id_id = e.id
WHERE m.date BETWEEN %s AND %s AND b.intext = false AND r.type_r != 'Bcc'
GROUP BY e.nom, e.prenom
having count(*) < %s; """, [date_debut, date_fin, seuil])

            rows33 = cursor.fetchall()

            liste7 = []
            for row in rows33:
                nom, prenom, nb_mails_envoyes = row
                liste7.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_envoyes': nb_mails_envoyes
                })

            liste7 = sorted(liste7, key=lambda x: x['nb_mails_envoyes'], reverse=True)
            liste77 = liste7[:10]

            if len(liste33) > 0 and len(liste77) > 0:

                DF1 = pd.DataFrame(liste33)
                DF2 = pd.DataFrame(liste77)
                trace1 = go.Bar(x=DF1['nom'], y=DF1['nb_mails_envoyes'], marker=dict(color='rgb(242, 65, 65)'),
                                name='Inerne')
                trace2 = go.Bar(x=DF2['nom'], y=DF2['nb_mails_envoyes'], marker=dict(color='rgb(47, 118, 128)'),
                                name='Externe')

                fig = go.Figure(data=[trace1, trace2])

                fig.update_layout(title=f'Principaux employés ayant envoyé moins de {seuil} mails', xaxis_title='Employés',
                                  yaxis_title='Nombre de mails envoyés', width=600, height=400, barmode='group')
                disp3 = plotly.offline.plot(fig, output_type='div')

            else:
                disp3 = []

        with connection.cursor() as cursor:
            cursor.execute("""SELECT t.nom, t.prenom, SUM(recus.nb_mails_recus) AS total_mails_recus
FROM (
    SELECT e.nom, e.prenom, a.id
    FROM monappli_employee e
    INNER JOIN monappli_adressemail a ON e.id = a.employee_id_id
) AS t
INNER JOIN (
    SELECT r.receiver_id, COUNT(*) AS nb_mails_recus
    FROM monappli_receiver r
    INNER JOIN monappli_mail m ON r.mail_id_id = m.id
    INNER JOIN monappli_adressemail a ON m.sender_id = a.id
    WHERE m.date BETWEEN %s AND %s AND r.type_r != 'Bcc' and a.intext = true
    GROUP BY r.receiver_id
    HAVING COUNT(*) < %s
) AS recus ON recus.receiver_id = t.id
GROUP BY t.nom, t.prenom;""", [date_debut, date_fin, seuil])
            rows4 = cursor.fetchall()

            liste4 = []
            for row in rows4:
                nom, prenom, nb_mails_recu = row
                liste4.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_recu': nb_mails_recu
                })

            liste4 = sorted(liste4, key=lambda x: x['nb_mails_recu'], reverse=True)
            liste44 = liste4[:10]

        with connection.cursor() as cursor:
            cursor.execute("""SELECT t.nom, t.prenom, SUM(recus.nb_mails_recus) AS total_mails_recus
FROM (
    SELECT e.nom, e.prenom, a.id
    FROM monappli_employee e
    INNER JOIN monappli_adressemail a ON e.id = a.employee_id_id
) AS t
INNER JOIN (
    SELECT r.receiver_id, COUNT(*) AS nb_mails_recus
    FROM monappli_receiver r
    INNER JOIN monappli_mail m ON r.mail_id_id = m.id
    INNER JOIN monappli_adressemail a ON m.sender_id = a.id
    WHERE m.date BETWEEN %s AND %s AND r.type_r != 'Bcc' and a.intext = false
    GROUP BY r.receiver_id
    HAVING COUNT(*) < %s
) AS recus ON recus.receiver_id = t.id
GROUP BY t.nom, t.prenom; """, [date_debut, date_fin, seuil])

            rows44 = cursor.fetchall()

            liste8 = []
            for row in rows44:
                nom, prenom, nb_mails_recu = row
                liste8.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_recu': nb_mails_recu
                })

            liste8 = sorted(liste8, key=lambda x: x['nb_mails_recu'], reverse=True)
            liste88 = liste8[:10]

            if len(liste44) > 0 and len(liste88) > 0:


                DF1 = pd.DataFrame(liste44)
                DF2 = pd.DataFrame(liste88)
                trace1 = go.Bar(x=DF1['nom'], y=DF1['nb_mails_recu'], marker=dict(color='rgb(242, 65, 65)'),
                                name='Inerne')
                trace2 = go.Bar(x=DF2['nom'], y=DF2['nb_mails_recu'], marker=dict(color='rgb(47, 118, 128)'),
                                name='Externe')
                fig = go.Figure(data=[trace1, trace2])

                fig.update_layout(title=f'Principaux employés ayant reçu moins de {seuil} mails', xaxis_title='Employés',
                                  yaxis_title='Nombre de mails reçus', width=600, height=400, barmode='group')
                disp4 = plotly.offline.plot(fig, output_type='div')

            else :
                disp4 = []



            context = {

                'liste3': liste3,
                'liste4': liste4,
                'liste1': liste1,
                'liste2': liste2,
                'date_debut': date_debut,
                'date_fin': date_fin,
                'seuil': seuil,
                'liste22': liste22,
                'disp1': disp1,
                'liste33': liste33,
                'disp2': disp2,
                'liste44': liste44,
                'disp4': disp4,
                'liste11': liste11,
                'disp3': disp3,
                'liste55': liste55,
                'liste6': liste6,
                'liste66': liste66,
                'liste7': liste7,
                'liste77': liste77,
                'liste8': liste8,
                'liste88': liste88,





            }
            return render(request, 'employeXmail.tmpl', context)
    else:
        return render(request, 'requete2.tmpl')



def requete3(request):
    employees = Employee.objects.all()
    context = {"employees": employees}
    return render(request, "requete3.tmpl", context=context)


def List_comu_empl(request):
    if request.method =='POST':
        id = request.POST.get('employe')
        employe = Employee.objects.get(id=id)
        employe_nom = employe.nom
        employe_prenom = employe.prenom
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')

        with connection.cursor() as cursor:
            cursor.execute("""SELECT DISTINCT e_receiver.nom ,e_receiver.prenom, count(e_receiver.id)
FROM monappli_employee e
INNER JOIN monappli_adressemail am ON e.id = am.employee_id_id
INNER JOIN monappli_mail m ON am.id = m.sender_id
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
INNER JOIN monappli_adresseMail am_receiver ON r.receiver_id = am_receiver.id
INNER JOIN monappli_employee e_receiver ON am_receiver.employee_id_id = e_receiver.id
WHERE 
    (e.nom = %s AND e.prenom = %s)
    AND m.date BETWEEN %s AND %s AND r.type_r != 'Bcc'
GROUP BY e_receiver.nom ,e_receiver.prenom;""", [employe_nom, employe_prenom, date_debut, date_fin])

            rows = cursor.fetchall()

            liste1 = []
            for row in rows:
                nom, prenom, nb_mails = row
                liste1.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails': nb_mails
                })

        with connection.cursor() as cursor:
            cursor.execute("""SELECT DISTINCT e_receiver.nom ,e_receiver.prenom, count(e_receiver.id)
FROM monappli_employee e
INNER JOIN monappli_adressemail am ON e.id = am.employee_id_id
INNER JOIN monappli_receiver r ON am.id = r.receiver_id
INNER JOIN monappli_mail m ON r.mail_id_id = m.id
INNER JOIN monappli_adresseMail am_receiver ON m.sender_id = am_receiver.id
INNER JOIN monappli_employee e_receiver ON am_receiver.employee_id_id = e_receiver.id
WHERE 
    (e.nom = %s AND e.prenom = %s)
    AND m.date BETWEEN %s AND %s AND r.type_r != 'Bcc'
GROUP BY e_receiver.nom ,e_receiver.prenom;""", [employe_nom, employe_prenom, date_debut, date_fin])

            rows2 = cursor.fetchall()

            liste2 = []
            for row in rows2:
                nom, prenom, nb_mails = row
                liste2.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails': nb_mails
                })

            from collections import defaultdict

            # Convertir liste1 et liste2 en dictionnaires où les clés sont les noms et prénoms
            dict_liste1 = {(employe['nom'], employe['prenom']): employe['nb_mails'] for employe in liste1}
            dict_liste2 = {(employe['nom'], employe['prenom']): employe['nb_mails'] for employe in liste2}

            # Initialiser un dictionnaire pour stocker les résultats
            dict_resultat = defaultdict(int)

            # Ajouter les valeurs de liste1 à dict_resultat
            for nom_prenom, nb_mails in dict_liste1.items():
                dict_resultat[nom_prenom] += nb_mails

            # Ajouter les valeurs de liste2 à dict_resultat
            for nom_prenom, nb_mails in dict_liste2.items():
                dict_resultat[nom_prenom] += nb_mails

            # Convertir le résultat en une liste de dictionnaires
            liste3 = [{'nom': nom, 'prenom': prenom, 'nb_mails': nb_mails} for (nom, prenom), nb_mails in
                      dict_resultat.items()]
            liste3 = sorted(liste3, key=lambda x: x['nb_mails'], reverse=True)

            liste33 = liste3[:10]

            if len(liste33)>0:

                DF = pd.DataFrame(liste33)
                fig = go.Figure(data=[go.Bar(x=DF['nom'], y=DF['nb_mails'], marker=dict(color='rgb(242, 65, 65)'), name=f'Employés ayant communiqué avec {employe_nom} {employe_prenom} entre le {date_debut} et le {date_fin}')])
                fig.update_layout(title=f'Top 10 des employés', xaxis_title='Employés',
                                  yaxis_title='Nombre de mails', width=1000, height=400,
                                    legend=dict(
                                        x=1.0,
                                        y=1.0,
                                        bgcolor='rgba(255, 255, 255, 0)',
                                        bordercolor='rgba(255, 255, 255, 0)'
                                    ), showlegend=True)
                disp = plotly.offline.plot(fig, output_type='div')

            else :
                disp = "Pas de données à afficher"

        context = {
            'liste1': liste1,
            'liste33' : liste33,
            'liste2': liste2,
            'employe_nom': employe_nom,
            'employe_prenom': employe_prenom,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'liste3': liste3,
            'disp': disp,
        }
        return render(request, 'List_comu_empl.tmpl', context)
    else:
        return render(request, 'requete3.tmpl')



def requete5(request):
    return render(request, 'requete5.tmpl',
                  {

                  })

def PgdNBmail(request):
    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        echange = request.POST.get('IntExt')

        if echange == 'Interne/Interne':
            with connection.cursor() as cursor:
                cursor.execute("""SELECT
    DATE_TRUNC('day', m.date) AS jour,
    COUNT(*) AS nombre_de_mails
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
WHERE m.date BETWEEN %s AND %s and a.intext = true and b.intext = true and r.type_r != 'Bcc'
GROUP BY jour
ORDER BY nombre_de_mails DESC;""", [date_debut, date_fin])
                rows = cursor.fetchall()

                liste = []
                for row in rows:
                    jour, nb_mails = row
                    liste.append({
                        'jour': jour,
                        'nb_mails': nb_mails
                    })
                liste = sorted(liste, key=lambda x: x['nb_mails'], reverse=True)
                liste1 = liste[:5]

                if len(liste1)>0:

                    DF = pd.DataFrame(liste1)
                    fig = go.Figure(data=[go.Bar(x=DF['jour'], y=DF['nb_mails'], marker=dict(color='rgb(242, 65, 65)'), name=f'Nombre de mails échangés {echange}')])
                    fig.update_layout(
                        title=f'Nombre de mails échangés entre employés internes entre le {date_debut} et le {date_fin}',
                        xaxis_title='Jour', yaxis_title='Nombre de mails échangés', width=1000, height=400,
                        legend=dict(
                            x=1.0,
                            y=1.0,
                            bgcolor='rgba(255, 255, 255, 0)',
                            bordercolor='rgba(255, 255, 255, 0)'
                        ), showlegend=True)
                    disp = plotly.offline.plot(fig, output_type='div')

                else :
                    disp = "Pas de données à afficher"


        elif echange == 'Interne/Externe':
            with connection.cursor() as cursor:
                cursor.execute("""SELECT
    DATE_TRUNC('day', m.date) AS jour,
    COUNT(*) AS nombre_de_mails
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
WHERE m.date BETWEEN %s AND %s and ((a.intext = false and b.intext = true) or (a.intext = true and b.intext = false)) and r.type_r != 'Bcc'
GROUP BY jour
ORDER BY nombre_de_mails DESC;""", [date_debut, date_fin])
                rows = cursor.fetchall()

                liste = []
                for row in rows:
                    jour, nb_mails = row
                    liste.append({
                        'jour': jour,
                        'nb_mails': nb_mails
                    })
                liste = sorted(liste, key=lambda x: x['nb_mails'], reverse=True)
                liste1 = liste[:10]

                DF= pd.DataFrame(liste1)
                fig=go.Figure(data=[go.Bar(x=DF['jour'],y=DF['nb_mails'],marker=dict(color='rgb(242, 65, 65)'),name=f'Nombre de mails échangés {echange}')])
                fig.update_layout(title=f'Nombre de mails échangés entre employés internes et externes entre le {date_debut} et le {date_fin}',xaxis_title='Jour',yaxis_title='Nombre de mails échangés',width=1000, height=400,legend=dict(
                        x=1.0,
                        y=1.0,
                        bgcolor='rgba(255, 255, 255, 0)',
                        bordercolor='rgba(255, 255, 255, 0)'
                    ), showlegend=True)
                disp=plotly.offline.plot(fig,output_type='div')

        else :
            with connection.cursor() as cursor:
                cursor.execute("""SELECT
    DATE_TRUNC('day', m.date) AS jour,
    COUNT(*) AS nombre_de_mails
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
WHERE m.date BETWEEN %s AND %s and ((a.intext = false and b.intext = true) or (a.intext = true and b.intext = false) or (a.intext = true and b.intext = true )) and r.type_r != 'Bcc'
GROUP BY jour
ORDER BY nombre_de_mails DESC;""", [date_debut, date_fin])

                rows = cursor.fetchall()

                liste = []
                for row in rows:

                    jour, nb_mails = row
                    liste.append({
                        'jour': jour,
                        'nb_mails': nb_mails
                    })
                liste = sorted(liste, key=lambda x: x['nb_mails'], reverse=True)
                liste1 = liste[:10]



                DF = pd.DataFrame(liste1)
                fig = go.Figure(data=[go.Bar(x=DF['jour'], y=DF['nb_mails'], marker=dict(color='rgb(242, 65, 65)'),name=f'Nombre de mails échangés {echange}')])
                fig.update_layout(
                    title=f'Nombre de mails échangés entre employés internes/externes et interne/interne entre le {date_debut} et le {date_fin}',
                    xaxis_title='Jour', yaxis_title='Nombre de mails échangés', width=1000, height=400,legend=dict(
                        x=1.0,
                        y=1.0,
                        bgcolor='rgba(255, 255, 255, 0)',
                        bordercolor='rgba(255, 255, 255, 0)'
                    ), showlegend=True)
                disp = plotly.offline.plot(fig, output_type='div')


        context = {
            'liste': liste,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'echange': echange,
            'disp': disp
        }

        return render(request, 'PgdNBmail.tmpl', context)
    else:
        return render(request, 'requete5.tmpl')




def requete6(request):
    return render(request, 'requete6.tmpl',
                  {

                  })

from django.db import connection

def Liste_mots(request):
    if request.method == 'POST':
        Type = request.POST.get('choix')
        nb_mots = int(request.POST.get('nbmot', 0))  # Récupérer le nombre de mots
        liste_mots = []  # Initialiser une liste pour stocker les mots entrés par l'utilisateur
        if nb_mots <= 0:
            return render(request, 'requete6.tmpl',
                   {

                   })
        else :
            # Parcourir les données du formulaire pour récupérer les mots saisis par l'utilisateur
            for i in range(1, nb_mots + 1):
                mot = request.POST.get(f'mot{i}', '')  # Récupérer le mot avec la clé dynamique mot{i}
                if mot:  # Vérifier si le champ n'est pas vide
                    liste_mots.append(mot)  # Ajouter le mot à la liste

            conditions = ' AND '.join([f"m.content LIKE '%{mot}%'" for mot in liste_mots])

            # Générer une liste de paramètres pour la requête SQL en fonction des mots saisis par l'utilisateur

            if Type == 'expediteur':

            # Construire la requête SQL avec des paramètres dynamique

                # Exécuter la requête SQL avec les paramètres dynamiques
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                    SELECT m.content, e.prenom, e.nom, m.subject, m.id
                    FROM monappli_mail m 
                    INNER JOIN monappli_adressemail a ON m.sender_id = a.id 
                    INNER JOIN monappli_employee e ON a.employee_id_id = e.id 
                    WHERE {conditions};
                """)
                    rows = cursor.fetchall()

                resultats = []
                for row in rows:
                    content, prenom, nom,subject, id = row
                    resultats.append({
                        'content': content,
                        'prenom': prenom,
                        'nom': nom,
                        'subject': subject,
                        'id': id
                    })

            else:

                # Exécuter la requête SQL avec les paramètres dynamiques
                with connection.cursor() as cursor:
                    cursor.execute(f"""select m.content, e.prenom, e.nom, m.subject, m.id from monappli_mail m
    inner join monappli_receiver r on m.id = r.mail_id_id
    inner join monappli_adressemail a on r.receiver_id = a.id
    inner join monappli_employee e on a.employee_id_id = e.id
    where {conditions};""")
                    rows = cursor.fetchall()

                resultats = []
                for row in rows:
                    content, prenom, nom, subject, id = row
                    resultats.append({
                        'content': content,
                        'prenom': prenom,
                        'nom': nom,
                        'subject': subject,
                        'id': id
                    })



            context = {
                'resultats': resultats,
                'Type': Type,
                'liste_mots': liste_mots

            }

            return render(request, 'Liste_mots.tmpl', context)

from django.shortcuts import render, get_object_or_404
def detail_mail(request, mail_id):
    mail = get_object_or_404(Mail, pk=mail_id)
    adressemail = AdresseMail.objects.filter(id=mail.sender_id).first()
    sender = Employee.objects.filter(id=adressemail.employee_id_id).first()
    return render(request, 'detail_mail.tmpl', {'mail': mail, 'sender': sender})


def requete7(request):
    employees = Employee.objects.all()
    context = {"employees": employees}
    return render(request, "requete7.tmpl", context=context)


def conv(request):
    if request.method =='POST':
        id1 = request.POST.get('employer')
        employer = Employee.objects.get(id=id1)
        employe_nom1 = employer.nom
        employe_prenom1 = employer.prenom
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        id2 = request.POST.get('employes')
        employes = Employee.objects.get(id=id2)
        employe_nom2 = employes.nom
        employe_prenom2 = employes.prenom

        with connection.cursor() as cursor:
            cursor.execute("""select m.id, m.content, m.subject, m.date from monappli_mail m
inner join monappli_receiver r on m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_employee e on a.employee_id_id = e.id
inner join monappli_adressemail b on r.receiver_id = b.id
inner join monappli_employee f on b.employee_id_id = f.id
where (f.id = %s and e.id = %s) or (f.id = %s and e.id = %s) and m.date between %s and %s
order by m.subject, m.date asc;
""", [id1, id2, id2,id1, date_debut, date_fin])

            rows = cursor.fetchall()

            liste1 = []
            for row in rows:
                id, content, subject, date = row
                liste1.append({
                    'id': id,
                    'content': content,
                    'subject': subject,
                    'date': date
                })

            grouped_emails = {}
            for row in rows:
                id, content, subject, date = row
                if subject not in grouped_emails:
                    grouped_emails[subject] = []
                grouped_emails[subject].append({'id': id, 'content': content, 'subject': subject, 'date': date})

        context = {
            'liste1': liste1,
            'grouped_emails': grouped_emails,

            'employe_nom1': employe_nom1,
            'employe_prenom1': employe_prenom1,
            'employe_nom2': employe_nom2,
            'employe_prenom2': employe_prenom2,
            'date_debut': date_debut,
            'date_fin': date_fin,
        }
        return render(request, 'conv.tmpl', context)
    else:
        return render(request, 'requete3.tmpl')

