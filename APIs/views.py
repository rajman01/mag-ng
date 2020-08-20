from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.authtoken.models import Token

from articles.models import ArticleModel
from .serializers import UserSerializer, ArticleSerializer, SearchSerializer
from .permissions import IsOwnerOrReadOnly

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'articles': reverse('articles', request=request, format=format),
        'signup': reverse('signup', request=request, format=format),
        'search':reverse('search', request=request, format=format),
    })

User = get_user_model()

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Profile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
        ]


class SignUpView(APIView):

    def post(self, request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleList(generics.ListCreateAPIView):

    search_fields = ['title', 'author']
    filter_backends = (filters.SearchFilter,)
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
        ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
        ]

class SearchList(generics.ListAPIView):
    serializer_class = SearchSerializer
    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        articles = ArticleModel.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        return articles