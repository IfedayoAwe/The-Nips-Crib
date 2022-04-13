from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

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