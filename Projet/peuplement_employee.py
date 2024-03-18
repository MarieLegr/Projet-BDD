import xml.etree.ElementTree as ET
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projet.settings')
django.setup()

from monappli.models import Employee, Category, AdresseMail



root = ET.parse('employes_enron.xml').getroot()

for emp in root.iter('employee'):

    employee = Employee()    
    employee.nom = emp.find('lastname').text
    employee.prenom = emp.find('firstname').text
    if emp.attrib:
        c = emp.get('category')
        category = Category()
        try :
            category = Category.objects.get(name=c)
        except :
            category.name = c
        category.save()
        employee.category_id = category
    employee.save()
    
    for email in emp.findall('email'):
        adresse = AdresseMail()
        adresse.adressemail = email.get('address')
        adresse.employee_id = employee
        adresse.intext = True
        adresse.save()
