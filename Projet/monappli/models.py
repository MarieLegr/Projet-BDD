from django.db import models


class category(models.Model):
    name = models.CharField(max_length=100)

    # category_id = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.name


class Employee(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    # emp_id = models.IntegerField(primary_key=True)
    category_fk = models.ForeignKey(category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.nom} {self.prenom}'


class IntExt(models.Model):
    internExtern = models.CharField(max_length=100)

    def __str__(self):
        return self.internExtern


class email(models.Model):
    email = models.EmailField()
    # email_id = models.IntegerField(primary_key=True)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    id_intext = models.ForeignKey(IntExt, on_delete=models.CASCADE)


    def __str__(self):
        return self.email




class Mail(models.Model):
    date = models.DateTimeField()
    subject = models.CharField(max_length=150)
    content = models.TextField()
    sender = models.ForeignKey(email, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} {self.content}'


class receiver(models.Model):
    receiver = models.ForeignKey(email, on_delete=models.CASCADE)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)




