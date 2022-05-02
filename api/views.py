from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from api.serializer import ImageSerialiser, PictureSerialiser, RegisterSerializer
from .image_renderer import JPEGRenderer
from imagestore.models import *
from rest_framework.response import Response
from PIL import Image, ImageOps
from utils.userpermission import IsAuthenticatedCustomer
from rest_framework.decorators import api_view
# Create your views here.



@api_view(['GET','POST'])
def customer_registration(request):
    

    if request.method == 'GET':
        profile = CustomUser.objects.all()
        serializer = RegisterSerializer(profile,many=True)
        return Response(serializer.data)

        
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Registration successfull'
            data['username'] = account.username
            data['email'] = account.email
           
         
   
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data,status=status.HTTP_201_CREATED)



class ImageList(generics.ListCreateAPIView):

    queryset = Images.objects.all()

    serializer_class = ImageSerialiser



class ImageApi(generics.RetrieveAPIView):

    renderer_classes = [JPEGRenderer]
    
    def get(self, request, *args, **kwargs):
        queryset = Images.objects.get(id=self.kwargs['id']).images
        data = queryset
        return Response(data, content_type='image/jpeg')


class ImageVariationApi(generics.RetrieveAPIView):

    sizes = {0:(100, 100), 1:(200, 200), 2:(300, 300), 3:(400, 400)}

    renderer_classes = [JPEGRenderer]

    def get(self, request, *args, **kwargs):

        queryset = Images.objects.get(id=self.kwargs['id']).images
        b = Image.open(queryset)

        # grayscale
        c = b.convert("L")
        c.save("img1.png")
        MAX_SIZE = (100, 100)

        image2 = b.copy()
        print(image2)

        image2.thumbnail(MAX_SIZE)
        print(image2)

        image2.save("media/images/d.jpg")
        image1 = Image.open("media/images/d.jpg")
        image1.show()

        # d.save("pythonthumb2.png")

        imagevariations.objects.create(
            image=Images.objects.first(),
            grayscale="media/images/img1.png",
            thumbnail="media/images/d.jpg"
        )
        for j,i in self.sizes.items():

            sized_image=b.resize(i)
            sized_image.save(f"media/images/size{j}.jpg")
            imagevariationssizes.objects.create(
                image=Images.objects.first(),
                sized_image=f"media/images/size{j}.jpg"
            )

        data = imagevariations.objects.first().grayscale
        

        return Response(data, content_type='image/jpeg')
