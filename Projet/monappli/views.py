from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from .models import Category
from .models import Mail
from .models import AdresseMail
from .models import Receiver
from .forms import SearchForm
from django.db import connection



def index(request):
    return render(request, "index.tmpl")

# Create your views here.
def index1(request):
    employees=Employee.objects.all()
    #category=Category.objects.all()
    context={"employees":employees}
    return render(request,"index1.tmpl",context=context)

def vue2(request):
    return HttpResponse("<p>Cette vue est une page d'aide basique pour l'application de mon projet.</p>") #<p> est un paragraphe en HTML

def vue3(request):
    response = HttpResponse() #Création d'une réponse HTTP
    response.write("<h1>Employee</h1>") #<h1> est un titre en HTML
    for cl in Employee.objects.all(): #Récupère tous les clients
        response.write(f"{cl}<br/>") #<br/> est un saut de ligne en HTML
    return response #Renvoie la réponse HTTP


def search_employee2(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            nom_employe = form.cleaned_data['nom_employe']
            employee = Employee.objects.filter(nom=nom_employe).first()

            category = Category.objects.filter(id=employee.category_id).first()
            context = {"employee": employee, "category": category}
            return render(request, "employee.tmpl", context=context)
    else:
        form = SearchForm()
    return render(request, 'index1.tmpl', {'form': form})


def search_employee(request):
    if request.method == 'POST':
        id=request.POST.get('employe')
        employe=Employee.objects.get(id=id)
        if employe.category_id_id is None:
            category=None
        else :
            category=Category.objects.get(id=employe.category_id_id)
        return render(request, 'employee.tmpl', {'employe': employe, 'category': category})
    else:
        return render(request,'index1.tmpl')


def vue4(request):
    employee = Employee.objects.all()
    category = Category.objects.all()
    context = {"employee": employee, "category": category}
    return render(request, "index1.tmpl", context=context)


def vue5(request):
    if request.method == 'POST':
        employe = request.POST.get('employe')

        return render(request, 'employee.tmpl', {'employe': employe})
    else:
        return render(request, 'index1.tmpl')


#requête sql

#test d'une vue qui affiche les employés qui ont une catégorie avec une requête sql
def vue6(request):
    employees = Employee.objects.raw('SELECT * FROM monappli_employee where category_id_id is not null')
    context = {"employees": employees}
    return render(request, "index1.tmpl", context=context)


#même chose que search_employee mais avec une requête sql
def search_employee3(request):
    if request.method == 'POST': # Si le formulaire est soumis
        employe_id = request.POST.get('employe') # Récupérer l'ID de l'employé

        with connection.cursor() as cursor: # Utiliser un curseur pour exécuter une requête SQL
            cursor.execute("""
                SELECT e.nom, e.prenom, e.category_id_id
                FROM monappli_employee e
                WHERE e.id = %s
            """, [employe_id]) # Exécuter la requête SQL avec l'ID de l'employé en paramètre
            row = cursor.fetchone() # Récupérer la première ligne du résultat, ici il y a seulement un employé

        if row: # Si une ligne a été trouvée
            nom, prenom, category_id = row # Récupérer les valeurs de la ligne
            # Récupérer le nom de la catégorie
            if category_id: # Si l'employé a une catégorie
                category = Category.objects.get(id=category_id)
                categorie_nom = category.name
            else:
                categorie_nom = "Aucune catégorie"

            context = {
                'nom': nom,
                'prenom': prenom,
                'categorie': categorie_nom,
            }
            return render(request, 'employee_details.tmpl', context)

    else:
        return render(request, 'index1.tmpl')


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
    return render(request, 'requete1.tmpl',
                  {

                  })

def attributs_employes(request):
    if request.method == 'POST':
        nom_employe = request.POST.get('nom_employe')
        prenom_employe = request.POST.get('prenom_employe')
        adresse_employe = request.POST.get('adresse_employe')

        if adresse_employe == "":
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.nom, e.prenom, c.name, am.adressemail
                    FROM monappli_employee e
                    LEFT JOIN monappli_category c ON e.category_id_id = c.id
                    LEFT JOIN monappli_adressemail am ON e.id = am.employee_id_id
                    WHERE e.nom = %s AND e.prenom = %s;
                """, [nom_employe, prenom_employe,])
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
                # Gérer le cas où aucun résultat n'est trouvé pour l'adresse email
                return HttpResponse("Aucun employé trouvé pour cette adresse email.")

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
                    coupleadress.append({
                        'adresse_employe': adresse_employe
                    })

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
                # Gérer le cas où aucun résultat n'est trouvé pour l'adresse email
                return HttpResponse("Aucun employé trouvé pour cette adresse email.")

  

def requete2(request):
    return render(request, 'requete2.tmpl',
                  {

                  })


def employeXmail(request):
    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        seuil = request.POST.get('seuil')

        with connection.cursor() as cursor:
            cursor.execute("""select e.nom, e.prenom,nb_mails_envoyes from monappli_employee e
inner join (select monappli_adressemail.employee_id_id, nb_mails_envoyes from monappli_adressemail
inner join
    (select sender_id, count(*) as nb_mails_envoyes
    from monappli_mail
    where date between %s and %s
    group by sender_id
    having count(*) > %s) as envoyes on envoyes.sender_id = monappli_adressemail.id
    where monappli_adressemail.employee_id_id is not null) as envoie2 on e.id = envoie2.employee_id_id;""", [date_debut, date_fin, seuil])
            rows1 = cursor.fetchall()


            liste1=[]
            for row in rows1:
                nom, prenom, nb_mails_envoyes = row
                liste1.append({
                    'nom': nom,
                    'prenom': prenom,
                    'nb_mails_envoyes': nb_mails_envoyes
                })


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
    WHERE m.date BETWEEN %s AND %s AND r.type_r != 'Bcc'
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

            #trier par odre decroissant
            liste2 = sorted(liste2, key=lambda x: x['nb_mails_recu'], reverse=True)
            liste22 = liste2[:10]



            context = {
                'liste1': liste1,
                'liste2': liste2,
                'date_debut': date_debut,
                'date_fin': date_fin,
                'seuil': seuil,
                'liste22': liste22,
            }
            return render(request, 'employeXmail.tmpl', context)
    else:
        return render(request, 'requete2.tmpl')



def requete3(request):
    employees = Employee.objects.all()
    # category=Category.objects.all()
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

        context = {
            'liste1': liste1,
            'liste2': liste2,
            'employe_nom': employe_nom,
            'employe_prenom': employe_prenom,
            'date_debut': date_debut,
            'date_fin': date_fin
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
WHERE m.date BETWEEN '2000-12-13' AND '2001-01-01' and a.intext = true and b.intext = true and r.type_r != 'Bcc'
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

        elif echange == 'IE':
            with connection.cursor() as cursor:
                cursor.execute("""SELECT
    DATE_TRUNC('day', m.date) AS jour,
    COUNT(*) AS nombre_de_mails
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
WHERE m.date BETWEEN '2000-12-13' AND '2001-01-01' and ((a.intext = false and b.intext = true) or (a.intext = true and b.intext = false)) and r.type_r != 'Bcc'
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

        else :
            with connection.cursor() as cursor:
                cursor.execute("""SELECT
    DATE_TRUNC('day', m.date) AS jour,
    COUNT(*) AS nombre_de_mails
FROM monappli_mail m
INNER JOIN monappli_receiver r ON m.id = r.mail_id_id
inner join monappli_adressemail a on m.sender_id = a.id
inner join monappli_adressemail b on r.receiver_id = b.id
WHERE m.date BETWEEN '2000-12-13' AND '2001-01-01' and ((a.intext = false and b.intext = true) or (a.intext = true and b.intext = false) or (a.intext = true and b.intext = true )) and r.type_r != 'Bcc'
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

        context = {
            'liste': liste,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'echange': echange
        }

        return render(request, 'PgdNBmail.tmpl', context)
    else:
        return render(request, 'requete5.tmpl')




def requete6(request):
    return render(request, 'requete6.tmpl',
                  {

                  })

def listemots(request):
    return render(request, 'requete6.tmpl',
                  {

                  })


        
        
    


