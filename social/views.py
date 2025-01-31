from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, GameAvailability, Profile, Friendship
from .forms import RegistrationForm, PostForm, CommentForm, GameAvailabilityForm, ProfileForm


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

@login_required
def profile(request, username=None):
    if username:
        # If a username is provided, show that user's profile
        user = get_object_or_404(User, username=username)
        profile, created = Profile.objects.get_or_create(user=user)
        is_own_profile = (user == request.user)  # Check if it's the logged-in user's profile
    else:
        # If no username is provided, show the logged-in user's profile
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        is_own_profile = True

    if is_own_profile and request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)  # Reload the updated profile page
    else:
        form = ProfileForm(instance=profile) if is_own_profile else None  # Only allow editing if it's their own profile
# Check if the logged-in user is friends with this user
    friendship_exists = Friendship.objects.filter(user=request.user, friend=user, accepted=True).exists()
    reverse_friendship_exists = Friendship.objects.filter(user=user, friend=request.user, accepted=True).exists()

    return render(request, 'social/profile.html', {
        'profile': profile,
        'user_profile': user,
        'form': form,
        'is_own_profile': is_own_profile,
        'friendship_exists': friendship_exists,
        'reverse_friendship_exists': reverse_friendship_exists
    })

# View to send a friend request
@login_required
def add_friend(request, username):
    # Get the user to be added as a friend
    user_to_add = get_object_or_404(User, username=username)

    # Prevent a user from adding themselves as a friend
    if user_to_add != request.user:
        # Ensure no duplicate friendship exists
        if not Friendship.objects.filter(user=request.user, friend=user_to_add).exists() and \
           not Friendship.objects.filter(user=user_to_add, friend=request.user).exists():
            # Create the friendship but mark it as unaccepted (False)
            Friendship.objects.create(user=request.user, friend=user_to_add, accepted=False)
    return redirect('profile', username=username)

# View to remove a friend
@login_required
def remove_friend(request, username):
    # Get the user to be removed as a friend
    user_to_remove = get_object_or_404(User, username=username)

    # Ensure the friendship exists before trying to remove it
    Friendship.objects.filter(user=request.user, friend=user_to_remove).delete()
    Friendship.objects.filter(user=user_to_remove, friend=request.user).delete()

    return redirect('profile', username=username)

@login_required
def accept_friend_request(request, username):
    # Get the user whose friend request is being accepted
    user_to_accept = get_object_or_404(User, username=username)

    # Find the friendship request
    friendship = Friendship.objects.filter(user=user_to_accept, friend=request.user).first()

    if friendship:
        friendship.accepted = True
        friendship.save()

    return redirect('profile', username=user_to_accept.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('home')  # Redirect back to home after commenting

    return redirect('home')  # If form is invalid, go back to home