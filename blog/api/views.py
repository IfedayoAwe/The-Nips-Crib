from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        BasePermission, 
                                        SAFE_METHODS)
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication

from blog.models import Post
from blog.api.serializers import PostSerializer

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ApiBlogListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated|ReadOnly]
    pagination_class = PageNumberPagination

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def post_list(request):

    if request.method == 'POST':
        user = request.user
        post = Post(author=user)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def post_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
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
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        context = {}
        post.delete()
        context['Deleted']="This content has been deletted"
        return Response(context, status=204)
