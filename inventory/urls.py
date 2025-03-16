from django.urls import path
from . import views

urlpatterns = [
    path("brand/", views.brand_view, name="brand"),
]