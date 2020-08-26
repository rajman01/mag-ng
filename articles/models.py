from django.db import models
from django.db.models import Q
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


def default_start_time():
    now = datetime.now()
    start = now.replace(hour=22, minute=0, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1)


categories_choices = (
    ('Art & Architecture', 'Art & Architecture'),
    ('Boating & Aviation', 'Boating & Aviation'),
    ('Business & Finance', 'Business & Finance'),
    ('Cars & Motorcycles', 'Cars & Motorcycles'),
    ('Celebrity & Gossip', 'Celebrity & Gossip'),
    ('Comics & Manga', 'Comics & Manga'),
    ('Crafts', 'Crafts'),
    ('Culture & Literature', 'Culture & Literature'),
    ('Family & Parenting', 'Family & Parenting'),
    ('Fashion', 'Fashion'),
    ('Food & Wine', 'Food & Wine'),
    ('Health & Fitness', 'Health & Fitness'),
    ('Home & Garden', 'Home & Garden'),
    ('Hunting & Fishing', 'Hunting & Fishing'),
    ('Kids & Teen', 'Kids & Teen'),
    ('Luxury', 'Luxury'),
    ('Men\'s Lifestyle', 'Men\'s Lifestyle'),
    ('Movies, Tv & Music', 'Movies, Tv & Music'),
    ('News & Politics', 'News & Politics'),
    ('Photography', 'Photography'),
    ('Science & Engineering', 'Science & Engineering'),
    ('Sports', 'Sports'),
    ('Tech & Gaming', 'Tech & Gaming'),
    ('Travel & Outdoor', 'Travel & Outdoor'),
    ('Women\'s Lifestyle', 'Women\'s Lifestyle'),
    ('Adult +18', 'Adult +18'),
)


class ArticleQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(date_posted__lte=now)

    def search(self, query):
        lookup = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__icontains=query) |
            Q(author__username__icontains=query)
        )
        return  self.filter(lookup)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


class ArticleModel(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(blank=True, null=True, upload_to='images/')
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)
    categories = models.CharField(max_length=50, choices=categories_choices, default='fashion')
    objects = ArticleManager()

    class Meta:
        ordering = ['-date_posted', '-updated', '-timestamp']

    def __str__(self):
        return self.title


class ImageModel(models.Model):
    article = models.ForeignKey(ArticleModel, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    image_description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.article.title


class TextModel(models.Model):
    article = models.ForeignKey(ArticleModel, default=None, on_delete=models.CASCADE)
    header = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.article.title


class SearchQuery(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query
