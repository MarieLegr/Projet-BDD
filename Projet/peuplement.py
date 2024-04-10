import os
import re
from datetime import datetime
import django
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projet.settings')
django.setup()

from monappli.models import Employee, Category, AdresseMail, Mail,  Receiver

#dossier = r'C:\Users\marie\Documents\GitHub\Projet-BDD\Projet\test'
dossier = r'C:\Users\marie\Desktop\Cours\BDD\projet\maildir'
#dossier = r'C:\Users\clara\Documents\M1\projet\maildir'

pattern_id = re.compile(r'Message-ID: <([\d.]+)\.JavaMail\.evans@thyme>')
pattern_receiver = re.compile(r'To:\s+([\w.-]+@[\w.-]+(?:,\s*[\w.-]+@[\w.-]+)*)')
pattern_receiver2 = re.compile(r'Cc:\s+([\w.-]+@[\w.-]+(?:,\s*[\w.-]+@[\w.-]+)*)')
pattern_receiver3 = re.compile(r'Bcc:\s+([\w.-]+@[\w.-]+(?:,\s*[\w.-]+@[\w.-]+)*)')
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
            with open(chemin_complet, 'r', encoding='latin1') as fichier:
                #print(f"Traitement du fichier : {chemin_complet}")
                contenu = fichier.read()

            match_id = re.search(pattern_id, contenu)
            match_receiver = re.search(pattern_receiver, contenu)
            match_receiver2 = re.search(pattern_receiver2, contenu)
            match_receiver3 = re.search(pattern_receiver3, contenu)
            match_Sujet = re.search(pattern_Sujet, contenu)
            match_date = re.search(pattern_date, contenu)
            match_sender = re.search(pattern_sender, contenu)
            match_contenu = re.search(pattern_contenu, contenu)


            #on vérifie que le mail n'est pas déjà dans la base de donnée
            if not Mail.objects.filter(message_id=match_id.group(1)).exists() :

                # remplissage table Mail()
                mail = Mail()

                if match_id:
                    mail.message_id = match_id.group(1)

                if match_date:
                    date_heure_str = match_date.group(1)
                    date_heure_obj = datetime.strptime(date_heure_str, "%a, %d %b %Y %H:%M:%S")
                    date_heure_obj = timezone.make_aware(date_heure_obj)
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
                    except ObjectDoesNotExist :
                        adresse.adressemail = ad
                        adresse.intext = "@enron" in ad
                        adresse.save()      

                    mail.sender = adresse

                mail.save()

                # remplissage table Receiver()
                if match_receiver:

                    ad = match_receiver.group(1)

                    for i in ad.split(","):
                        i = i.strip()
                        receiver = Receiver()
                        receiver.mail_id = mail
                        receiver.type_r = "To"

                        adresse = AdresseMail()

                        try :
                            adresse = AdresseMail.objects.get(adressemail=i)
                        except ObjectDoesNotExist:
                            adresse.adressemail = i
                            adresse.intext = "@enron" in i
                            adresse.save()

                        receiver.receiver = adresse
                        receiver.save()


                if match_receiver2:

                    ad = match_receiver2.group(1)

                    for i in ad.split(","):
                        i = i.strip()
                        receiver = Receiver()
                        receiver.mail_id = mail
                        receiver.type_r = "Cc"

                        adresse = AdresseMail()

                        try :
                            adresse = AdresseMail.objects.get(adressemail=i)
                        except ObjectDoesNotExist:
                            adresse.adressemail = i
                            adresse.intext = "@enron" in i
                            adresse.save()

                        receiver.receiver = adresse
                        receiver.save()


                if match_receiver3:

                    ad = match_receiver3.group(1)

                    for i in ad.split(","):
                        i = i.strip()
                        receiver = Receiver()
                        receiver.mail_id = mail
                        receiver.type_r = "Bcc"

                        adresse = AdresseMail()

                        try :
                            adresse = AdresseMail.objects.get(adressemail=i)
                        except ObjectDoesNotExist:
                            adresse.adressemail = i
                            adresse.intext = "@enron" in i
                            adresse.save()

                        receiver.receiver = adresse
                        receiver.save()



parcourir_dossier(dossier)