from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('main/', views.main, name="home"),
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('friends/', views.access_wall, name="wall"),
    path('user/<int:user_id>/', views.display_user, name="display"),
    path('user/<int:user_id>/remove/', views.remove, name="remove"),
    path('user/<int:user_id>/add/', views.add, name="add"),
    path('logout/', views.logout, name="logout"),
]