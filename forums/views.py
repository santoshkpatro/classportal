from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from forums.models import Post, Comment

from . forms import PostCreateForm


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'forums/post_list.html', {'posts': posts})


@login_required(login_url='login')
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if not form.is_valid():
            messages.warning(request, 'Invalid form details')
            return redirect('forums_post_list')

        new_post = Post(**form.cleaned_data)
        new_post.user = request.user
        new_post.save()

    return redirect('forums_post_list')


@login_required(login_url='login')
def post_comment_add(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            comment_text = request.POST['comment_text']
            Comment.objects.create(user=request.user, post=post, comment_text=comment_text)

            messages.success(request, 'Comment added!')
            return redirect('forums_post_list')
        except Post.DoesNotExist:
            messages.warning(request, 'Post does not exist')
    return redirect('forums_post_list')