# The-Nips-Crib

## Description
This repository contains the the code that each file in the project directory of building a social website with a full registration and authentication system, query functions to get a particular post from the list view and all posts of a particular author, a search function to locate a particular post or user, CRUD operations to create, read, update and delete posts, create function is given only to registered persons, update and delete permissions are given to the owner of the post. Password reset using email and the default django email service, ability to upload profile pictures, update profile picture, username and email by the user, pagination of all search results and queries and the corresponding API VIEWS all of all functions in the same repository.
The project is designed as intended for usage in a production environment either with templates or as api endpoints using token authentication. The program consists of a custom made User model, a Profile model for the users profile and Post model for posts made.


## Features
* Authentication: This consists of a user registration and login feature. In the users directory of this repository consists of a register-view in the views.py file, the template register.html in templates\users and the correspondiing url. The default UserCreationForm in django was modified to contain an email field and named UserRegistrationForm in the forms.py file.
Once the POST request is made to the url and form is validated using my custom made User moedel in the models.py file, the user would be created, a profile would be automatically generated using signals in the signals.py file and then redirected to the login page and would be able to login.
Also, a user can only view the home page but will be redirected to login if he/she tries to view the post_detail page or user_post page if not logged, same with the site visitors.

* Authentication API View: Once a POST requst has been made to the url, the data would be serialized using my custom made RegistrationSerializer and then validated and saved. Once saved, a token would be automatically generated as this programs API view uses a token authentication and a Profile would also be generated for that user using the @receiver signal and the user would be able to login. if a user's email contains any uppercase letter it would be converted to all lowercase before it is being saved, if a user tries to login with an email containing uppercase, it would be converted to lowercase and then logged in. 

* Query Functions: In this project is a search function "search_post" in the blog/views.py file with the ability to locate a particular post if the searched word is contained in any post with the author, title or content. The post request is stored in a session to enable pagination of the searched result.
The ability to query and display all posts made by a particular user
The ability to get a particular post from all posts displayed on the home screen.
note: results are paginated by 10

* Query API Function: API view to query functions above were implemented.

* CRUD functions on posts: Class based views were used in the blog/views.py file to implement CRUD operations on posts. Non registered users as well as loggedout users can only view the home page but would be redirected to login if any other operation was attempted. Logged in users can only update and delete posts made by them.

* CRUD functions API View: The CRUD operations here are designed just like the one above with a few modifications. Before requests can be serialized or validated, the token generated must be granted permissions to carry out such operations.

* Password Reset Function: This uses the default django PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView and sends a reset link to the users email.

* Password Reset API: API view to reset password, if forgotten. It sends the token to the email of the user which can then be tested in postman..

* Profile CRUD operations: The program includes the ability for a user to update their username, email and profile pictures although a default profile picture is given once the user is created.

* Profile CRUD operations API: The program includes the API view for a user to update their username, email and profile pictures although a default profile picture is given once the user is created. If a user's email contains uppercase, it would be converted to all lowercase, an aspect ratio of 1:1 and size maximum 2mb is compulsory for profile picture updates.

* Change Password API View: A function and serializer to change a users password is implemented in this program. It checks if the old password is correct and makes a comparison between the new_password and confirm_new_password before it sets the user's password to the new password inputed.


## Language
The Nips Crib was built in Python using the Django framework and also the Django Rest framework for the corresponding API VIEWS.


## Dependencies
asgiref==3.5.0
distlib==0.3.4
Django==4.0.2
django-crispy-forms==1.14.0
djangorestframework==3.13.1
filelock==3.4.2
Pillow==9.0.1
platformdirs==2.4.1
pytz==2022.1
six==1.16.0
sqlparse==0.4.2
tzdata==2021.5
virtualenv==20.13.0


## Post Man Documentation
A list of the endpoints and the functions they implement can be found in the API folder inside every app folder.
Note: Set url in django_blog/urls.py to api by commenting out "path('', include('blog.urls'))" and commenting urls in restframework section and vice versa.

app_name = 'users'

urlpatterns = [
    path('register/', registration_view, name='register-api'),
    path('properties/', user_properties_view, name='properties-api'),
    path('profile', user_profile_view, name='profile-api'),
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('login/', ObtainAuthTokenView.as_view(), name='login-api'),
	path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]

app_name = 'blog'

urlpatterns = [
    path('post/<int:pk>/', post_detail, name='post-api-detail'),
    path('post/', new_post, name='post'),
    path('', ApiBlogListView.as_view(), name='list'),
    path('user/<str:username>', UserApiBlogListView.as_view(), name='user-api-posts'),
]

1. 'list', send a GET request with no authentication or permissions should return all posts by all users if there is any.
2. 'register-api' to register a new user, send a POST request, set keys: username, email, password, password2 and their corresponding values in body of request. A "response": "Sucessfully registered a new user.", "email", "username" and "token" would be returned.
3. 'login-api' to login. The login uses a custom made ObtainAuthTokenView class view which extends from the APIView, Paste token in header of request although a token is created once logged in and set keys: username and password in body. Note: value of key "username" would be the email of the registered user this is due to django's default "USERNAME_FIELD".
4. 'list' and set request to 'POST' to create a new post, paste the token in the header and set keys: title and content in body.
5. 'post-api-detail'. Paste the token in the header, the url and id of a post and send a GET request to get that post.
6. 'post/<id of a post made with the same user token>'. set keys: title and content / title or content and send a PUT request to update the post, either a title or content must be inputed to make an update, the title would remain the same as the previous if a new one wasn't given, likewise the content.
7. 'post/<id of a post made with the same user token>'. send a DELET request to delete the post.
8. To query all posts made by a particular user, an authentication token must be provided in the head of the request.
9. The url 'properties' points to the functions that update the user's 'username and email' respectively. An authentication token would be required in the header of the request and the corresponding values to the keys: 'username and email', a user can choose to update only the username or email or both, likewise is postman.
10. The url 'profile-api' points to the functions that update the user's 'profile picture'. An authentication token would be required in the header of the request and the corresponding values to the key: 'image', and then the new file
11. To use the change_password function, an authentication token is needed, an old_password, new_password and confirm_password key is necessary.
12. To reset password, the email is needed, a new token would be sent to the User's email, keys: 'token and password' would be needed to set the new password.
13. To logout, the email is required, a request is sent and the current token would be deleted, the user would need to login again to generate a new token.

## Contribution
Pull requests are and new features suggestions are welcomed.
I also plan on adding more features and API's to this project.