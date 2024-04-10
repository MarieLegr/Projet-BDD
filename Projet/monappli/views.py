from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from .models import Category
from .models import Mail
from .models import AdresseMail
from .models import Receiver


# Create your views here.
def index(request):
    employee=Employee.objects.all()
    category=Category.objects.all()
    context={"employee":employee,"category":category}
    return render(request,"index.tmpl",context=context)
def vue2(request):
    return HttpResponse("<p>Cette vue est une page d'aide basique pour l'application de mon projet.</p>") #<p> est un paragraphe en HTML

def vue3(request):
    response = HttpResponse() #Création d'une réponse HTTP
    response.write("<h1>Employee</h1>") #<h1> est un titre en HTML
    for cl in Employee.objects.all(): #Récupère tous les clients
        response.write(f"{cl}<br/>") #<br/> est un saut de ligne en HTML
    return response #Renvoie la réponse HTTP


def search_employee(request,nom):
    employee=Employee.objects.filter(nom=nom).first()
    category=Category.objects.filter(id=employee.category_id).first()
    context={"employee":employee,"category":category}
    return render(request,"employee.tmpl",context=context)