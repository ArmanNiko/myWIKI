from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>+create", views.create, name="create"),
    path("<str:title>", views.show, name="show"),
]
