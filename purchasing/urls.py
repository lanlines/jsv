from django.urls import path
from . import views

urlpatterns = [
    path("supplier", views.supplier_view, name="supplier"),
    path("purchase", views.purchase_view, name="purchase"),
    path("purchase-list", views.purchase_list_view, name="purchase_list"),
]