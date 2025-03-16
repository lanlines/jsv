from django.db import models
from accounts.models import CustomUser  # Import the CustomUser model from the accounts app
# Create your models here.cx


class Requisition(models.Model):
    OWNER = 'owner'
    WAREHOUSE_MANAGER = 'warehouse_manager'
    SHOP_ATTENDANT = 'shop_attendant'
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (WAREHOUSE_MANAGER, 'Warehouse Manager'),
        (SHOP_ATTENDANT, 'Shop Attendant'),
    ]

    requested_by = models.CharField(max_length=20, choices=ROLE_CHOICES)
    requested_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('purchase', 'Purchase')
    ], default='pending')
    status_changed_by = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Requisition {self.id} by {self.requested_by}"    
    
class RequisitionItem(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='items')
    item_requested = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    brand = models.ForeignKey('inventory.Brand', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item_requested} - {self.quantity}"
    
