from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from .models import Category
from .models import Mail
from .models import AdresseMail
from .models import Receiver
from .forms import SearchForm
from django.db import connection



# Create your views here.
def index(request):
    employees=Employee.objects.all()
    #category=Category.objects.all()
    context={"employees":employees}
    return render(request,"index.tmpl",context=context)

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
    return render(request, 'index.tmpl', {'form': form})


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
        return render(request,'index.tmpl')


def vue4(request):
    employee = Employee.objects.all()
    category = Category.objects.all()
    context = {"employee": employee, "category": category}
    return render(request, "index.tmpl", context=context)


def vue5(request):
    if request.method == 'POST':
        employe = request.POST.get('employe')

        return render(request, 'employee.tmpl', {'employe': employe})
    else:
        return render(request, 'index.tmpl')


#requête sql

#test d'une vue qui affiche les employés qui ont une catégorie avec une requête sql
def vue6(request):
    employees = Employee.objects.raw('SELECT * FROM monappli_employee where category_id_id is not null')
    context = {"employees": employees}
    return render(request, "index.tmpl", context=context)


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
        return render(request, 'index.tmpl')
