from django.urls import path, include
from users.api.views import (
                            registration_view, 
                            user_properties_view, 
                            user_profile_view,
                            does_account_exist_view,
                            ObtainAuthTokenView,
                            ChangePasswordView
                            )

app_name = 'users'

urlpatterns = [
    path('register/', registration_view, name='register-api'),
    path('properties/', user_properties_view, name='properties-api'),
    path('profile', user_profile_view, name='profile-api'),
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('login/', ObtainAuthTokenView.as_view(), name='login-api'),
	path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]