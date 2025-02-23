from django.urls import path
from . import views

urlpatterns = [
    path('requisition-view/', views.requisitions_view, name='requisitions'),
    path('create-requisition/', views.create_requisition_view, name='create_requisition'),
    #path("", views.index, name="login"),
    # path("", views.login_view, name="login_view"),
    # path("add-user/", views.add_user_view, name="add_user"),
]