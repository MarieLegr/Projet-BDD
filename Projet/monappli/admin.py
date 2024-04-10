from django.contrib import admin
from .models import Employee
from .models import Category
from .models import Mail
from .models import AdresseMail
from .models import Receiver

# Register your models here.
admin.site.register(Employee)
admin.site.register(Category)
admin.site.register(Mail)
admin.site.register(AdresseMail)
admin.site.register(Receiver)
