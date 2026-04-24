from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'asset_id', 'author', 'created_at', 'view_count')
    search_fields = ('title', 'content')
    list_filter = ('asset_id',)
