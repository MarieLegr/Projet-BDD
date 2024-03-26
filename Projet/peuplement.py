import os
import re
from datetime import datetime
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projet.settings')
django.setup()

from monappli.models import Employee, Category, AdresseMail, Mail,  Receiver

dossier = r'C:\Users\clara\Documents\GitHub\Projet-BDD\Projet\test'

pattern_receiver = re.compile(r'To:\s+([\w.-]+@[\w.-]+)')
pattern_receiver2 = re.compile(r'Cc:\s+([\w.-]+@[\w.-]+)')
pattern_receiver3 = re.compile(r'Bcc:\s+([\w.-]+@[\w.-]+)')
pattern_Sujet = re.compile(r'^Subject: (.+)$', re.MULTILINE)
pattern_date = re.compile(r'Date: ([A-Z][a-z]+, \d{1,2} [A-Z][a-z]+ \d{4} \d{2}:\d{2}:\d{2})')
pattern_sender = re.compile(r'From:\s+([\w.-]+@[\w.-]+)')
pattern_contenu = re.compile(r'X-FileName:[ \S]*\n\n([\s\S]+)')




def parcourir_dossier(dossier):
    # Parcourir tous les fichiers et dossiers dans le dossier donné
    for element in os.listdir(dossier):
        # Obtenir le chemin complet de l'élément
        chemin_complet = os.path.join(dossier, element)

        # Vérifier si l'élément est un dossier
        if os.path.isdir(chemin_complet):
            # Si c'est un dossier, appeler récursivement la fonction pour parcourir ce dossier
            parcourir_dossier(chemin_complet)
        else:
            # Sinon, c'est un fichier
            with open(chemin_complet, 'r', encoding='utf-8') as fichier:
                contenu = fichier.read()

            match_receiver = re.search(pattern_receiver, contenu)
            match_receiver2 = re.search(pattern_receiver2, contenu)
            match_receiver3 = re.search(pattern_receiver3, contenu)
            match_Sujet = re.search(pattern_Sujet, contenu)
            match_date = re.search(pattern_date, contenu)
            match_sender = re.search(pattern_sender, contenu)
            match_contenu = re.search(pattern_contenu, contenu)





            # remplissage table Mail()
            mail = Mail()

            if match_date:
                # Extraire la date et l'heure de la correspondance
                date_heure_str = match_date.group(1)
                # Format de la chaîne de caractères
                format_date_heure = "%a, %d %b %Y %H:%M:%S"
                # Convertir la chaîne de caractères en objet datetime
                date_heure_obj = datetime.strptime(date_heure_str, format_date_heure)
                # Afficher l'objet datetime
                mail.date = date_heure_obj

            if match_Sujet:
                mail.subject = match_Sujet.group(1)

            if match_contenu:
                mail.content = match_contenu.group(1)

            
            if match_sender:

                adresse = AdresseMail()  
                ad = match_sender.group(1)  
                try:
                    adresse = AdresseMail.objects.get(adressemail=ad)   
                except :
                    adresse.adressemail = ad
                    adresse.intext = "@enron" in ad
                    adresse.save()      

                mail.sender = adresse
                mail.save()

            if match_receiver:

                receiver = Receiver()
                receiver.mail_id = mail
                receiver.type_r = "To"

                adresse = AdresseMail()
                ad = match_receiver.group(1)
                try :
                    adresse = AdresseMail.objects.get(adressemail=ad) 
                except:
                    adresse.adressemail = ad 
                    adresse.intext = "@enron" in ad
                    adresse.save()   
                
                receiver.receiver = adresse
                receiver.save()

            if match_receiver2:

                receiver = Receiver()
                receiver.mail_id = mail
                receiver.type_r = "Cc"

                adresse = AdresseMail()
                ad = match_receiver2.group(1)
                try :
                    adresse = AdresseMail.objects.get(adressemail=ad) 
                except:
                    adresse.adressemail = ad 
                    adresse.intext = "@enron" in ad
                    adresse.save()    
                
                receiver.receiver = adresse 
                receiver.save()          

            if match_receiver3:

                receiver = Receiver()
                receiver.mail_id = mail
                receiver.type_r = "Bcc"

                adresse = AdresseMail()
                ad = match_receiver3.group(1)
                try :
                    adresse = AdresseMail.objects.get(adressemail=ad) 
                except:
                    adresse.adressemail = ad 
                    adresse.intext = "@enron" in ad
                    adresse.save()    
                
                receiver.receiver = adresse 
                receiver.save()   



parcourir_dossier(dossier)