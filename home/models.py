from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.user.username
    

class Attendance(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="Present")
    def __str__(self):
        return self.student.user.username

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=20)
#     email = models.EmailField(max_length=254)
#     phoneno =models.IntegerField(max_length=10)
#     country = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     district = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)
#     password = models.CharField(max_length=50)    
#     def __str__(self) -> str:
#         return self.name
    