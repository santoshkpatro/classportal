from django.shortcuts import render
from forums.models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'forums/post_list.html', {'posts': posts})