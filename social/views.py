from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, GameAvailability
from .forms import RegistrationForm, PostForm, CommentForm, GameAvailabilityForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'social/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'social/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    availability = GameAvailability.objects.all()
    return render(request, 'social/home.html', {'posts': posts, 'availability': availability})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'social/create_post.html', {'form': form})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)  # Ensure the post belongs to the logged-in user

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page after updating
    else:
        form = PostForm(instance=post)  # Pre-fill the form with the current post content

    return render(request, 'social/update_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)  # Ensure the post belongs to the logged-in user
    post.delete()  # Delete the post
    return redirect('home')  # Redirect to the home page after deleting the post

@login_required
def update_game_status(request):
    try:
        status = GameAvailability.objects.get(user=request.user)
    except GameAvailability.DoesNotExist:
        status = None
    
    if request.method == 'POST':
        form = GameAvailabilityForm(request.POST, instance=status)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.save()
            return redirect('home')
    else:
        form = GameAvailabilityForm(instance=status)
    return render(request, 'social/update_game_status.html', {'form': form})