from rest_framework import serializers
from .models import *



class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        
        
        

class GusetSerializers(serializers.ModelSerializer): 
    class Meta:
        model = Guest
        fields = '__all__'
        
        
        
        
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'               
        
        
        
class PostSerializer(serializers.ModelSerializer):
     class Meta:
        model = Post
        fields = '__all__'  