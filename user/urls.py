from django.urls import path, include

from user import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.PostListView.as_view(), name = 'blog-home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.loginView, name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', user_views.logoutView, name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name = 'users/password_reset.html'
             ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name = 'users/password_reset_done.html'
             ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name = 'users/password_reset_confirm.html'
             ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name = 'users/password_reset_complete.html'
             ),
         name='password_reset_complete'),
    
    
    # Student urls
    path('blogs/', user_views.StudentPostListView.as_view(), name = 'student'),
    path('videos/', user_views.student_video_index, name = 'video'),
    
    
    # Moderators urls
    path('moderators/', user_views.moderator, name = 'moderator'),
    path('videos/', user_views.moderator_video_index, name = 'moderate-video'),

    
]