from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    descriptio = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datacompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '- by ' +self.user.username
    
class Certificado(models.Model):
    fecha = models.DateTimeField(null=True,blank=True)
    completo = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha + '- by ' +self.user.username