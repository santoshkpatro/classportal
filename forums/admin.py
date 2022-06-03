from django.contrib import admin
from . models import Post, Comment


class CommentAdminInline(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']
    inlines = [CommentAdminInline]