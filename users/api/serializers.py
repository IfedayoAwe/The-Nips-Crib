import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
from rest_framework import serializers
from users.models import User, Profile
from users.utils import is_image_aspect_ratio_valid, is_image_size_valid

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

			# Check image size
                if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                    os.remove(url)
                    raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

                # Check image aspect ratio
                if not is_image_aspect_ratio_valid(url):
                    os.remove(url)
                    raise serializers.ValidationError({"response": "Image width and height must be equal"})                

                os.remove(url)
            except KeyError:
                pass
            return profile

class ChangePasswordSerializer(serializers.Serializer):

	old_password 				= serializers.CharField(required=True)
	new_password 				= serializers.CharField(required=True)
	confirm_new_password 		= serializers.CharField(required=True)