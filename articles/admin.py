from django.contrib import admin
from .models import ArticleModel, ImageModel, TextModel


class ArticleImageAdmin(admin.StackedInline):
    model = ImageModel
    extra = 1


class ArticleTextAdmin(admin.StackedInline):
    model = TextModel
    extra = 1


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageAdmin, ArticleTextAdmin]

    class Meta:
        model = ArticleModel


admin.register(ImageModel,ArticleImageAdmin)


admin.register(TextModel,ArticleTextAdmin)