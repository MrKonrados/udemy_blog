from django.contrib import admin
from .models import Post, Tag, Category
from django.utils.translation import gettext as _

def make_published(modeladmin, request, queryset):
    queryset.update(status="published")
    make_published.short_description = _('Zmień status na Opublikowano')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'author', 'created', 'updated', 'status')
    prepopulated_fields = {'slug': ('title',), }
    list_filter = ('author', 'status')
    actions = [make_published]

@admin.register(Tag, Category)
class TagCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
