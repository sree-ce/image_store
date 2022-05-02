
from rest_framework import serializers
from imagestore.models import CustomUser, Images



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
    
        fields = ['name','password','email','username']

    def save(self):

        password = self.validated_data['password']
        

        if password is None:
            raise serializers.ValidationError({'error': 'password cannot be empty'})

        

        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        account = CustomUser(email=self.validated_data['email'], username=self.validated_data['username'],name = self.validated_data['name'])
        account.set_password(password)
        account.save()
        
        
        return account


class ImageSerialiser(serializers.ModelSerializer):

    

    class Meta:
        model = Images
        fields = "__all__"



class PictureSerialiser(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Images
        fields = ('images')

    def get_image_url(self, obj):
        return obj.images.url