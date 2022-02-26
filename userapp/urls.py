from unicodedata import name
from django.urls import path
from . import views

app_name = "userapp"

urlpatterns = [

    # authenticate
    path("", views.register, name="register"),
    path("login/", views.signIn, name="signIn"),
    path("logout/", views.signOut, name="signOut"),

    # account
    path("dashboard/", views.dashboard, name="dashboard"),
    path('dashboard/edit/', views.editDashboard, name="editDashboard"),

    # skills
    path('skill/', views.create_skill, name='create_skill'),
    path('skill/update/<str:skill_id>/', views.update_skill, name='update_skill'),
    path('skill/delete/<str:skill_id>/', views.delete_skill, name='delete_skill'),



    # profiles
    path('profile/',views.profiles, name="profiles"),
    path("<str:username>/", views.userProfile, name='userProfile'),
]