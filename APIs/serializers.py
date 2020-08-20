from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser
from articles.models import ArticleModel

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):

    #email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    articles = serializers.HyperlinkedRelatedField(
        view_name='detail', 
        read_only=True,
        many=True)
    

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        #user.set_password(validated_data['password'])
        #user.save()
        return user

    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','password','articles']
        read_only_fields = ['id',]
        
class ArticleSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = ArticleModel
        fields = ['url','id','author','title','cover_image','date_posted','description','category','publish']

class SearchSerializer(serializers.HyperlinkedModelSerializer):

    def to_native(self, obj):
        if isinstance(obj, ArticleModel):
            serializer = ArticleSerializer(obj)
        elif isinstance(obj, User):
            serializer = UserSerializer(obj)
        else:
            raise Exception("%s not found" %(obj))
        return serializer.data
    class Meta:
        model = ArticleModel