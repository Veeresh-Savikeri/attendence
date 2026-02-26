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
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="Present")
    def __str__(self):
        return f"{self.student.user.username} - {self.staff.user.username}"
