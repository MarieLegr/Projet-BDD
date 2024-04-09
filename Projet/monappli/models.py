from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.nom} {self.prenom}'


class AdresseMail(models.Model):
    adressemail = models.EmailField(max_length=150)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    intext = models.BooleanField(null=True)


    def __str__(self):
        return self.adressemail


class Mail(models.Model):
    message_id = models.CharField(max_length=50, unique=True, null=True)
    date = models.DateTimeField()
    subject = models.CharField(max_length=300,null=True)
    content = models.TextField()
    sender = models.ForeignKey(AdresseMail, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.date} {self.subject} {self.content}'


class Receiver(models.Model):
    receiver = models.ForeignKey(AdresseMail, on_delete=models.CASCADE)
    mail_id = models.ForeignKey(Mail, on_delete=models.CASCADE)
    type_r = models.CharField(max_length=5) # To, Cc, Bcc

    def __str__(self):
        return self.type_r



