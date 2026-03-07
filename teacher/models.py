from django.db import models
from django.contrib.auth.models import User
from home.models import *

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    batchcode =models.CharField(max_length=50,null=True,blank=True)
    branch = models.CharField(max_length=50,null=True,blank=True)
    mode = models.CharField(max_length=10,null=True,blank=True)
    def __str__(self):
        return self.user.username
    
    
class Attendance(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    session = models.ForeignKey('Session',on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.user.username}"

class Session(models.Model):
    batchcode = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    mode = models.CharField(max_length=10)
    started = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.batchcode}-{self.subject}"