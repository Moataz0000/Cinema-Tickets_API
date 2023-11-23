from django.contrib import admin
from django.urls import path , include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests' , views.Viewsets_Guest),
router.register('movies' , views.Viewsers_Movie),
router.register('reservation' , views.Viewsets_Reservation),


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #1 not uesd rest framework and model
    path('djanog/jsonresponse/' , views.no_rest),
    
    #2 not used rest framework but i ues my model
    path('django/jsonresponse/frommodel/' , views.no_rest_from_model), 
    
    #3 GET POST from restframework function based view @api_view
    path('rest/api/' , views.FBV_List),
    
    #4 used GET and PUT and Delete and restframework
    path('rest/api/<int:pk>' , views.FBV_PK), 
    
    # 5 GET and POST from restframework class based view APIView
    path('rest/cbv/' , views.CBV_List.as_view()),
    
    # 5 GET  and PUT and DELETE from restframework class based view APIView
    path('rest/cbv/<int:pk>' , views.CBV_ALL_List.as_view()),

    # GET , POST from restframwork class based view mixins
    path('rest/mixins/' , views.Mixins_List.as_view()),
    
    # GET , PUT , DELETE from restframework class based view mixins
    path('rest/mixins/<int:pk>/' , views.Mixins_pk.as_view()),
    
    # GUT , POST , From restframework class besed view Generics
    path('rest/generics/' , views.Generics_List.as_view()),
    
    # GUT , PUT , DELETE , Frokm restframework class based view Generics 
    path('rest/generics/<int:pk>/' , views.Generics_pK.as_view()),
    
    # Viewsets
    path('rest/viewsets/' , include(router.urls)),
    
    
    # Find Movie
    path('rest/findmovie/', views.find_movie),
    
    # New Reservation
    path('fbv/newreservation/' , views.New_reservation),
    
    # Rest auth url
    path('api-auth' , include('rest_framework.urls')), # Log out
    
    # Token Authentication 
    path('api-token-auth' , obtain_auth_token),
    
    # Post pk generics
    # path('post/genercis/'),
    path('post/genercis/<int:pk>' , views.Post_pk.as_view())
    
]
