from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm, ReplyForm, CommentForm, SearchForm
from .models import Blog, Comment, Reply
from django.contrib import messages
from django.db.models import Count
import json

# Create your views here.

@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, f'{blog.title} posted on disc platform')
            return redirect('add_blog')
    else:
        form = BlogForm()
    return render(request, 'blogs/add_blogs.html', {'form': form})


@login_required
def view_blogs(request):
    # Initialize forms
    comment_form = CommentForm()
    reply_form = ReplyForm()
    search_form = SearchForm(request.GET or None)

    # Handle search functionality
    query = None
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')

    # Filter blogs based on search query if provided
    if query:
        data = Blog.objects.filter(title__icontains=query) | Blog.objects.filter(description__icontains=query)
    else:
        data = Blog.objects.all()

    if request.method == "POST":
        if 'comment' in request.POST:
            blog_id = request.POST.get('blog_id')
            blog = get_object_or_404(Blog, id=blog_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.blog = blog
                comment.save()
                return redirect('view_blogs')
        elif 'reply' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.user = request.user
                reply.comment = comment
                reply.save()
                return redirect('view_blogs')

    return render(request, 'blogs/view_blog.html', {
        'data': data,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'search_form': search_form,
    })


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this blog")

    if request.method == "POST":
        blog.delete()
        return redirect('view_blogs')

    return render(request, 'blogs/confirm_delete.html', {'blog': blog})


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog")

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('view_blogs')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blogs/edit_blog.html', {'form': form, 'blog': blog})


@login_required
def view_your_blogs(request):
    data = Blog.objects.filter(user=request.user)
    if request.method == 'GET':
        q = request.GET.get('search_own')
        if q != None:
            data = Blog.objects.filter(user=request.user, title__icontains=q)
    return render(request, 'blogs/view_your_blogs.html', {'data': data})


@login_required
def analytics_view_blogs(request):
    # Get total blogs
    total_blogs = Blog.objects.count()

    # Get total comments
    total_comments = Comment.objects.count()

    # Get active blogs
    active_blogs = Blog.objects.filter(active=True).count()

    # Get inactive blogs
    inactive_blogs = Blog.objects.filter(active=False).count()

    # Get number of blogs per user
    blogs_per_user = Blog.objects.values('user__username').annotate(count=Count('id')).order_by('-count')

    # Prepare context data
    context = {
        'total_blogs': total_blogs,
        'total_comments': total_comments,
        'active_blogs': active_blogs,
        'inactive_blogs': inactive_blogs,
        'blogs_per_user': list(blogs_per_user),
    }

    return render(request, 'blogs/analytics_view_blogs.html', context)


@login_required
def analytics_view_blogs_user(request):
    # Get total blogs for logged-in user
    total_blogs = Blog.objects.filter(user=request.user).count()

    # Get total comments for logged-in user
    total_comments = Comment.objects.filter(blog__user=request.user).count()

    # Get active blogs for logged-in user
    active_blogs = Blog.objects.filter(user=request.user, active=True).count()

    # Get inactive blogs for logged-in user
    inactive_blogs = Blog.objects.filter(user=request.user, active=False).count()

    # Get number of blogs per user
    blogs_per_user = Blog.objects.values('user__username').annotate(count=Count('id')).order_by('-count')

    # Prepare context data
    context = {
        'total_blogs': total_blogs,
        'total_comments': total_comments,
        'active_blogs': active_blogs,
        'inactive_blogs': inactive_blogs,
        'blogs_per_user': list(blogs_per_user),
    }

    return render(request, 'blogs/analytics_view_blogs_user.html', context)