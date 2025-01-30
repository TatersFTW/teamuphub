from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('update-post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update-game-status/', views.update_game_status, name='update_game_status'),
    path('profile/', views.profile, name='profile'),
]