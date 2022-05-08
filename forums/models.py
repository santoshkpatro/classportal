import uuid
from django.db import models
from django.conf import settings


class Post(models.Model):
    STATUS_CHOICES = (
        (0, 'Published'),
        (1, 'Draft')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_posts', on_delete=models.CASCADE)
    post_text = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'posts'


    def __str__(self) -> str:
        return self.post_text



class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comments', on_delete=models.CASCADE)
    question = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    comment_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'comments'


    def __str__(self) -> str:
        return self.comment_text