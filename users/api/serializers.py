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