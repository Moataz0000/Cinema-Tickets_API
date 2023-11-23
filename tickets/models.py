from django.db import models
from django.db.models import signals 
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User






# Cuest -- Movie -- Reservation 



class Movie(models.Model):
    hall = models.CharField(max_length=15)
    movie = models.CharField(max_length=70)
    data = models.DateField()
    
    def __str__(self):
        return self.movie
    
    
class Guest(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50) 
    
    
    
    def __str__(self):
        return self.name
    
    
    
       
class Reservation(models.Model):
    guest = models.ForeignKey(Guest,on_delete=models.CASCADE , related_name='reservation')
    movie = models.ForeignKey(Movie , on_delete=models.CASCADE , related_name='reservation')
    
    def __str__(self):
        return self.guest
    
    
    
class Post(models.Model):
    auther = models.ForeignKey(User , on_delete=models.CASCADE)    
    title = models.CharField(max_length=50)
    body = models.TextField()
    
    
    # def __str__(self):
    #     return self.auther
    
    
# signals 

# Define a signal handler function
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    # Check if a new user instance is created
    if created:
        # If yes, create a new authentication token for the user
        Token.objects.create(user=instance)