from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser
from articles.models import ArticleModel, ImageModel, TextModel

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):

    #email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    articlemodel_set = serializers.HyperlinkedRelatedField(
        view_name='articlemodel-detail',
        read_only=True,
        many=True)
    

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            # first_name=validated_data['first_name'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        #user.set_password(validated_data['password'])
        #user.save()
        return user

    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'username', 'password', 'articlemodel_set', ]
        read_only_fields = ['id',]
        
class ImageSerializer(serializers.HyperlinkedModelSerializer):

    article = serializers.ReadOnlyField(source='article.title')
    # article = serializers.HyperlinkedRelatedField(view_name='articles', read_only=True)

    class Meta:
        model = ImageModel
        fields = ['url', 'id', 'article', 'image', 'image_description', 'timestamp']

class TextSerializer(serializers.HyperlinkedModelSerializer):

    article = serializers.ReadOnlyField(source='article.title')
    # article = serializers.HyperlinkedRelatedField(view_name='articles', read_only=True)


    class Meta:
        model = TextModel
        fields = ['url', 'id', 'article', 'header', 'text', 'timestamp']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')
    # article = serializers.HyperlinkedRelatedField(view_name='articles', read_only=True)
    imagemodel_set = serializers.HyperlinkedRelatedField(
        view_name='imagemodel-detail',
        read_only=True,
        many=True)
    textmodel_set = serializers.HyperlinkedRelatedField(
        view_name='textmodel-detail',
        read_only=True,
        many=True)

    class Meta:
        model = ArticleModel
        fields = ['url', 'id', 'author', 'title', 'cover_image', 'date_posted', 'description', 'categories', 'publish', 'imagemodel_set', 'textmodel_set']

# class SearchSerializer(serializers.HyperlinkedModelSerializer):
#
#     def to_native(self, obj):
#         if isinstance(obj, ArticleModel):
#             serializer = ArticleSerializer(obj)
#         elif isinstance(obj, User):
#             serializer = UserSerializer(obj)
#         else:
#             raise Exception("%s not found" %(obj))
#         return serializer.data
#     class Meta:
#         model = ArticleModel