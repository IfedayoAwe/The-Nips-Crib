import cv2
import sys
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
from rest_framework import serializers
from users.models import User, Profile

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwarga = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'passwords must match!'})
        user.set_password(password)
        user.save()
        return user

class UserPropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =['pk', 'email', 'username']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields =['image']

    def validate(self, profile):
            try:
                
                image = profile['image']
                url = os.path.join(settings.TEMP , str(image))
                storage = FileSystemStorage(location=url)

                with storage.open('', 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()

                if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
                    os.remove(url)
                    raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

                img = cv2.imread(url)
                dimensions = img.shape # gives: (height, width, ?)
                
                aspect_ratio = dimensions[1] / dimensions[0] # divide w / h
                if aspect_ratio != 1:
                    os.remove(url)
                    raise serializers.ValidationError({"response": "Image must be 1:1. Try a different image."})

                os.remove(url)
            except KeyError:
                pass
            return profile