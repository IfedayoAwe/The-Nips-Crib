# The-Nips-Crib

## Description
This repository contains the the code that each file in the project directory of building a social website with a full registration and authentication system, query functions to get a particular post from the list view and all posts of a particular author, a search function to locate a particular post or user, CRUD operations to create, read, update and delete posts, create function is given only to registered persons, update and delete permissions are given to the owner of the post. Password reset using email and the default django email service, ability to upload profile pictures, update profile picture, username and email by the user, pagination of all search results and queries and the corresponding API VIEWS all of all functions in the same repository.
The project is designed as intended for usage in a production environment either with templates or as api endpoints using token authentication. The program consists of a custom made User model, a Profile model for the users profile and Post model for posts made.


## Features
* Authentication
This consists of a user registration and login feature. In the users directory of this repository consists of a register-view in the views.py file, the template register.html in templates\users and the correspondiing url. The default UserCreationForm in django was modified to contain an email field and named UserRegistrationForm in the forms.py file.
Once the POST request is made to the url and form is validated using my custom made User moedel in the models.py file, the user would be created, a profile would be automatically generated using signals in the signals.py file and then redirected to the login page and would be able to login.
Also, a user can only view the home page but will be redirected to login if he/she tries to view the post_detail page or user_post page if not logged, same with the site visitors.

* Authentication API View
Once a POST requst has been made to the url, the data would be serialized using my custom made RegistrationSerializer and then validated and saved. Once saved, a token would be automatically generated as this programs API view uses a token authentication and a Profile would also be generated for that user using the @receiver signal and the user would be able to login.

* Query Functions
In this project is a search function "search_post" in the blog/views.py file with the ability to locate a particular post if the searched word is contained in any post with the author, title or content. The post request is stored in a session to enable pagination of the searched result.
The ability to query and display all posts made by a particular user
The ability to get a particular post from all posts displayed on the home screen.
note: results are paginated by 10

* CRUD functions on posts
Class based views were used in the blog/views.py file to implement CRUD operations on posts. Non registered users as well as loggedout users can only view the home page but would be redirected to login if any other operation was attempted. Logged in users can only update and delete posts made by them.

* CRUD functions API View
The CRUD operations here are designed just like the one above with a few modifications. Before requests can be serialized or validated, the token generated must be granted permissions to carry out such operations.

* Password Reset Function
This uses the default django PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView and sends a reset link to the users email.

* Profile CRUD operations
The program includes the ability for a user to perform CRUD operations on their profile pictures although a default profile picture is given once the user is created, also ability to Update their username and email.


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
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login')
]


app_name = 'blog'

urlpatterns = [
    path('', post_list, name='blog-home'),
    path('post/<int:pk>/', post_detail, name='post-detail'),
    path('list/', ApiBlogListView.as_view(), name='list')
]

1. Run the server and go to 'list/', send a GET request with no authentication or permissions should return all posts by all users if there is any.
2. Go to 'register/' to register a new user, send a POST request to set keys: username, email, password, password2 and their corresponding values in body of request. A "response": "Sucessfully registered a new user.", "email", "username" and "token" would be returned.
3. Go to 'login/' to login. Paste token in header of request and set keys: username and password in body. Note: value of key "username" would be the email of the registered user this is due to django's default "USERNAME_FIELD".
4. Go to '' and set request to 'POST' to create a new post, paste the token in the header and set keys: title and content in body.
5. Go to 'post/<id of any post>/'. Paste the token in the header and send a GET request to get that post.
6. Go to 'post/<id of a post made with the same user token>'. set keys: title and content and send a PUT request to update the post.
7. Go to 'post/<id of a post made with the same user token>'. send a DELET request to delete the post.


## Contribution
Pull requests are welcome.
