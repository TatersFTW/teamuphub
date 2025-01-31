from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'), # Login
    path('home/', views.home, name='home'), # Home
    path('register/', views.register, name='register'), # Register
    path('login/', views.user_login, name='login'), # Login
    path('logout/', views.user_logout, name='logout'), # Logout
    path('create-post/', views.create_post, name='create_post'), # Create post
    path('update-post/<int:post_id>/', views.update_post, name='update_post'), # Update post
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'), # Delete post
    path('update-game-status/', views.update_game_status, name='update_game_status'), # Update game status  
    path('profile/', views.profile, name='profile'), # Profile URL
    path('profile/<str:username>/', views.profile, name='profile'),
    path('add-friend/<str:username>/', views.add_friend, name='add_friend'),  # Add friend
    path('remove-friend/<str:username>/', views.remove_friend, name='remove_friend'),  # Remove friend
    path('accept-friend-request/<str:username>/', views.accept_friend_request, name='accept_friend_request'), # Accept friend request
     path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),  # Add comment URL
]