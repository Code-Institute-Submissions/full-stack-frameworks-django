from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Post
from .forms import BlogPostForm
from django.contrib.auth.models import User

@login_required
def get_posts(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blogposts.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, 'postdetail.html', {'post': post})

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_or_edit_post(request, pk=None):

    post = get_object_or_404(Post, pk=pk) if pk else None
    
    if post is not None:
        if request.user.username != post.author:
            return redirect(post_detail, post.pk)

    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogpostform.html', {'form': form})    

