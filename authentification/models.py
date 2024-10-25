from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    password_confirmation = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, default='')  
    
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username
    class Meta:
        app_label = 'authentification'  



class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    country = models.CharField(max_length=100, default='')  
    county = models.CharField(max_length=100, default='')   
    city = models.CharField(max_length=100, default='')     
    postal_code = models.CharField(max_length=20, default='')  
    street = models.CharField(max_length=255, default='')  
    phone = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.user.username



class SomeOtherModel(models.Model):
    user = models.ForeignKey('authentification.CustomUser', on_delete=models.PROTECT)
   

    def __str__(self):
        return f"{self.user} - {self.some_field}"  

class Psychologist(models.Model):
    name = models.CharField(max_length=100)
    therapy_type = models.CharField(max_length=100)
    cv = models.TextField()
    image = models.ImageField(upload_to='psychologists/', blank=True, null=True)

    def __str__(self):
        return self.name

    
class Review(models.Model):
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} on {self.created_at}'


class Appointment(models.Model):
    full_name = models.CharField(max_length=100, default='John Doe')
    email = models.EmailField(default='example@example.com')
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()