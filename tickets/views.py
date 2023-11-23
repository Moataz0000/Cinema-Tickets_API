from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from.serializers import *
from rest_framework import status,filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly


# Without REST and no model query FBV

def no_rest(request):
    
    guests = [
        {
            'id' : 1,
            'name' : 'mezo',
            'mobile' : 5482694
            
            
        },
        {
            'id' : 2,
            'name' : 'moataz',
            'mobile' : 7854589
        }
        
    ]
    
    
    return JsonResponse   (guests , safe=False)


# model data defult django without rest
def no_rest_from_model(request):
    
    # My data
    data = Guest.objects.all()  # endpoint
    
    # List of data
    response = {
        'guests': list(data.values('name' , 'mobile'))
    }
    
    return JsonResponse(response)
    


# Function based views
@api_view(['GET' , 'POST']) # the decorator is Handel methods 
def FBV_List(request):
    
    # GET 
    if request.method == 'GET':
        guests = Guest.objects.all() # All data in database
        serializer = GusetSerializers(guests , many=True).data
        return Response(serializer)
        
    
    # POST 
    elif request.method == 'POST': 
        """ 
        POST method is create data 
        steps : 
        check if return request method type == POST 
        the data in request come on serializer then 
        go to data base .
        then check if serializer is valid ?
        if serializer is valid seve serializer
        """
        serializer = GusetSerializers(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.data,status.HTTP_400_BAD_REQUEST)
    
    

  # Function based views  

# Function based views GET , PUT , DELETE
@api_view(['GET' , 'PUT' , 'DELETE'])
def FBV_PK(request , pk):
    try:
       # GET 
       gusets = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
       
       
       
    if request.method == 'GET':
        serializer = GusetSerializers(gusets)
        return Response(serializer.data)
    
    
    # PUT = Update
    elif request.method == 'PUT':
        serializer = GusetSerializers(gusets , data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    
    # DELETE 
    if request.method == 'DELETE':
        gusets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
    
    
# CBV Class beased views GET , POST
class CBV_List(APIView):
    def get(self , request):
        guest = Guest.objects.all()
        serializer = GusetSerializers(guest , many=True)
        return Response(serializer.data)
    
    
    
    def post(self , request):
      
        serializer =  GusetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
               
    
    
    
    
    
# class based view ---> pk | ( GET , PUT , DELETE )    
class CBV_ALL_List(APIView):
    # this fun get only get object 
    def get_objects(self , pk ):
        try:
            return Guest.objects.get(pk=pk)
        # if object == it object and if not in object == Http404
        except Guest.DoesNotExist:
            raise Http404
    #  GET    
    def get(self , request , pk):
        guest = self.get_objects(pk)    
        serializer = GusetSerializers(guest)
        return Response(serializer.data)
    
    # PUT
    def put(self , request , pk):
        guest = self.get_objects(pk)
        serializer = GusetSerializers(guest , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
    
    
    # DELETE 
    def delete(self , request , pk):
        guest = self.get_objects(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

            
        
        
    
    


# Mixins List { mixins.ListModelMixin , mixins.CreateModelMixin } ==> esey write my code and 
# [ generics.GenericAPIView ] ==> Response API  GET , POST
class Mixins_List(mixins.ListModelMixin , mixins.CreateModelMixin , generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerializers
    
    def get(self , request):
        return self.list(request)
    
    def post(self , request):
        return self.create(request)
    
# Mixins  
# GET , POST , DELETE with PK  
class Mixins_pk(mixins.RetrieveModelMixin , mixins.UpdateModelMixin , mixins.DestroyModelMixin , generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerializers
    
    def get(self , reqeust , pk):
        return self.retrieve(reqeust)
    
    
    def put(self , reqeust , pk):
        return self.update(reqeust)
    
    def delete(self , request , pk):
        return self.destroy(request)
        
    

    
    
 
# Generics [ GET , POST  ]
class Generics_List(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerializers
    # Secuer API | Perrmissions
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    
# Generics [ GET , PUT , DELETE ] 

class Generics_pK(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerializers
    # Secuer API | Perrmissions
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    
    
    
# Viewsets  :

# Guest    
class Viewsets_Guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GusetSerializers
    
# Movie   
class Viewsers_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filter_backends = [filters.SearchFilter]
    seaech_fields = ['movie']
    
# Reservation     
class Viewsets_Reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
            
            
            
            
@api_view(['GET'])
def find_movie(requset):
    movie = Movie.objects.filter(
        hall = requset.data['hall'],
        movie = requset.data['movie'],
       
    )            
    serializer = MovieSerializers(movie , many=True)
    return Response(serializer.data)



@api_view(['POST'])
def New_reservation(requset):
    try:
        movie = Movie.objects.get(
        hall=requset.data['hall'],
        movie=requset.data['movie'],
       )
    except Movie.DoesNotExist:
       return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    # New Guest
    guest = Guest()
    guest.name = requset.data['name']
    guest.mobile = requset.data['mobile']
    guest.save()
    
    # New Reservation
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    
    serializer = ReservationSerializer(reservation , many=True)
    
    return Response( serializer.data ,tatus=status.HTTP_201_CREATED)

    
    
# Post author editor 
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    