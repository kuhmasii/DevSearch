from unicodedata import name
from django.urls import path
from . import views

app_name = "newapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("project/<str:detail_id>",views.detail, name="detail"),
    path('project/create/', views.create_project, name="create_project"),
    path("project/update/<str:detail_id>/", views.update_project, name="update_project"),
    path("project/delete/<str:detail_id>/", views.delete_project, name="delete_project"),
]
