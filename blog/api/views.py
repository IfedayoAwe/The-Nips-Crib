from django.shortcuts import get_object_or_404
from users.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
                                        IsAuthenticated,
                                        BasePermission, 
                                        SAFE_METHODS
                                        )
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from blog.models import Post
from blog.api.serializers import (
                                  PostSerializer,
                                  PostUpdateSerializer, 
                                  PostCreateSerializer
                                  )

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ApiBlogListView(ListAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated|ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__username']


class UserApiBlogListView(ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def new_post(request):
    if request.method == 'POST':
        request_data = request.data
        data = request_data.copy()
        data['author'] = request.user.pk
        serializer = PostCreateSerializer(data=data)
        data = {}
    if serializer.is_valid():
        post = serializer.save()
        data['response'] = 'created'
        data['pk'] = post.pk
        data['title'] = post.title
        data['body'] = post.content
        data['date_updated'] = post.date_posted
        data['username'] = post.author.username
        return Response(data=data)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def post_detail(request, pk):

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    user = request.user
    if post.author != user:
        return Response({'response': "You don't have permissions to edit that!"})

    elif request.method == 'PUT':
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Updated'
            data['pk'] = post.pk
            data['title'] = post.title
            data['content'] = post.content
            data['post_updated'] = post.date_updated
            data['username'] = post.author.username
            return Response(data=data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        context = {}
        post.delete()
        context['Deleted']="This content has been deletted"
        return Response(context, status=204)