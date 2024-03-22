import os
import re
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projet.settings')
django.setup()

from monappli.models import Employee, Category, AdresseMail, Mail,  Receiver

dossier = r'C:\Users\marie\Desktop\Cours\BDD\test\allen-p'

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
            # Sinon, c'est un fichier, vous pouvez faire ce que vous voulez avec le fichier ici
            print(f"Traitement du fichier : {chemin_complet}")
            with open(chemin_complet, 'r', encoding='utf-8') as fichier:
                contenu = fichier.read()

            match_receiver = re.search(pattern_receiver, contenu)
            match_receiver2 = re.search(pattern_receiver2, contenu)
            match_receiver3 = re.search(pattern_receiver3, contenu)
            match_Sujet = re.search(pattern_Sujet, contenu)
            match_date = re.search(pattern_date, contenu)
            match_sender = re.search(pattern_sender, contenu)
            match_contenu = re.search(pattern_contenu, contenu)

            mail = Mail()
            receiver = Receiver()

            # Afficher le résultat
            if match_sender:
                sender = match_sender.group(1)
                mail.sender = sender

            if match_receiver:
                r = match_receiver.group(1)
                print(f"Expéditeur : {r}")

            if match_receiver2:
                r = match_receiver2.group(1)
                print(f"Expéditeur : {r}")

            if match_receiver3:
                r = match_receiver3.group(1)
                print(f"Expéditeur : {r}")

            if match_Sujet:
                Sujet = match_Sujet.group(1)
                mail.sujet = Sujet

            if match_date:
                # Extraire la date et l'heure de la correspondance
                date_heure_str = match_date.group(1)
                # Format de la chaîne de caractères
                format_date_heure = "%a, %d %b %Y %H:%M:%S"
                # Convertir la chaîne de caractères en objet datetime
                date_heure_obj = datetime.strptime(date_heure_str, format_date_heure)
                # Afficher l'objet datetime

                mail.date = date_heure_obj

            if match_contenu:
                contenu = match_contenu.group(1)
                mail.contenu = contenu


            print("-" * 50)



parcourir_dossier(dossier)