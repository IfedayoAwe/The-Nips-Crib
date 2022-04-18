from rest_framework.views import APIView
from django.contrib.auth import authenticate
from users.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.api.serializers import RegistrationSerializer, UserPropertiesSerializer, UserProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

@api_view(['POST'])
@permission_classes((AllowAny,))
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Sucessfully registered a new user."
            data['email'] = user.email
            data['username'] = user.username
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
        serializer = UserPropertiesSerializer(user, data=request.data)
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
			context['email'] = email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)