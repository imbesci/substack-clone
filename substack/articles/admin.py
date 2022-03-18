from faulthandler import register
from django.contrib import admin
from .models import Article
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class ArticleAdmin(UserAdmin):
    ordering = ('title',)
    list_display = ('title', 'author', 'topic', 'date', 'slug', 'views', 'is_draft')
    search_fields = ('title', 'author', 'date')
    readonly_fields = ('author', 'date', 'slug', 'last_edited')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(Article, ArticleAdmin)