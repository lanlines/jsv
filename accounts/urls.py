from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="login"),
    path("", views.login_view, name="login_view"),
    path("add-user/", views.add_user_view, name="add_user"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("users/", views.users_view, name="users"),
    path('logout/', views.logout_view, name='logout'),
]