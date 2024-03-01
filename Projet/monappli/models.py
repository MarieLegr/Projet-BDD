from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.nom} {self.prenom}'


class IntExt(models.Model):
    internExtern = models.CharField(max_length=100)

    def __str__(self):
        return self.internExtern


class Email(models.Model):
    email = models.EmailField()
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    intext_id = models.ForeignKey(IntExt, on_delete=models.CASCADE)


    def __str__(self):
        return self.email


class Mail(models.Model):
    date = models.DateTimeField()
    subject = models.CharField(max_length=150)
    content = models.TextField()
    sender = models.ForeignKey(Email, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} {self.subject} {self.content}'


class Receiver(models.Model):
    receiver = models.ForeignKey(Email, on_delete=models.CASCADE)
    mail_id = models.ForeignKey(Mail, on_delete=models.CASCADE)
    type_r = models.CharField(max_length=100)

    def __str__(self):
        return self.type_r



