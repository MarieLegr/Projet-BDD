from django.db import models
class Employee(models.Model):
    name = models.CharField(max_length=100)
    emp_id = models.IntegerField()
    def __str__(self):
        return self.name

class email(models.Model):
    email = models.EmailField()
    email_id = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class mailbody(models.Model):
    subject = models.TextField()
    date = models.DateTimeField()
    content = models.TextField()
    sender = models.ForeignKey(email, on_delete=models.CASCADE)

class mailreceiver(models.Model):
    receiver = models.EmailField()
    mail = models.ForeignKey(mailbody, on_delete=models.CASCADE)