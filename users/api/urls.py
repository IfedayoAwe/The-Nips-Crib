from django.urls import path
from users.api.views import (
                            registration_view, 
                            user_properties_view, 
                            user_profile_view, 
                            ObtainAuthTokenView
                            )

app_name = 'users'


urlpatterns = [
    path('register/', registration_view, name='register-api'),
    path('login/', ObtainAuthTokenView.as_view(), name='login-api'),
    path('properties/', user_properties_view, name='properties-api'),
    path('profile/', user_profile_view, name='profile-api')
]