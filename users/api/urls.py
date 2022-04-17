from django.urls import path
from users.api.views import registration_view, user_properties_view, user_profile_view
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'


urlpatterns = [
    path('register/', registration_view, name='register-api'),
    path('login/', obtain_auth_token, name='login-api'),
    path('properties/', user_properties_view, name='properties-api'),
    path('profile/', user_profile_view, name='profile-api')
]