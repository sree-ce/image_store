from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import ImageApi,ImageVariationApi,ImageList
from .views import customer_registration



urlpatterns = [ 
    path('signup/',customer_registration,name='customer_registration'),

    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

    path('addimage/',ImageList.as_view()),
    
    path('original/<int:id>/',ImageApi.as_view()),
    path('variation/<int:id>/',ImageVariationApi.as_view()),
   
    
]