from rest_framework.views import APIView
from django.contrib.auth import authenticate
from users.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from users.api.serializers import (
                                    RegistrationSerializer, 
                                    UserPropertiesSerializer, 
                                    UserProfileSerializer, 
                                    ChangePasswordSerializer
                                    )
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView

@api_view(['POST'])
@permission_classes((AllowAny,))
def registration_view(request):
    if request.method == 'POST':
        request_data = request.data
        data = request_data.copy()
        data['email'] = request.data['email'].lower()
        serializer = RegistrationSerializer(data=data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Sucessfully registered a new user."
            data['email'] = user.email.lower()
            data['username'] = user.username
            data['pk'] = user.pk
            data['token'] = Token.objects.get(user = user).key
        else:
            data = serializer.errors
        return Response(data)

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def user_properties_view(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = UserPropertiesSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        data = request.data
        if 'email' in request.data:
            request_data = request.data
            data = request_data.copy()
            data['email'] = request.data['email'].lower()
        serializer = UserPropertiesSerializer(user, data=data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account update success"
            return Response(data=data)
        return Response(serializer.errors, status=404)

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def user_profile_view(request):
    try:
        profile = request.user.profile
    except User.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "profile update success"
            return Response(data=data)
        return Response(serializer.errors, status=404)

class ObtainAuthTokenView(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}
		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)

		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email.lower()
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'
		return Response(context)

@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):
    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            user = User.objects.get(email=email)
            data['response'] = email
        except User.DoesNotExist:
            data['response'] = "Account does not exist"
        return Response(data)

class ChangePasswordView(UpdateAPIView):
	serializer_class = ChangePasswordSerializer
	model = User
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=400)
			# confirm the new passwords match
			new_password = serializer.data.get("new_password")
			confirm_new_password = serializer.data.get("confirm_new_password")
			if new_password != confirm_new_password:
				return Response({"new_password": ["New passwords must match"]}, status=400)
			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"response":"successfully changed password"}, status=200)

		return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response('User Logged out successfully')
        except:
            return Response(status=400)