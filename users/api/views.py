from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token

#you never allow registration oh!
#E  dey affect am from settings
@api_view(['POST'])
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