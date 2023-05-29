from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('details/<str:user>/', views.details, name='details'),
    path('detail-art/<int:id>/', views.detail_art, name='detail-art'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('art-post/', views.art_post, name='art-post'),
    path('user-create/', views.user_create, name='user-create'),
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('edit-profile/<int:id>/', views.user_profile_edit, name='edit-profile'),
    path('verify/<str:user>/', views.verify_user, name='verify')
]