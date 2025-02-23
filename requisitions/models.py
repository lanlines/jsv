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


    item_requested = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    requested_by = models.CharField(max_length=20, choices=ROLE_CHOICES)
    requested_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    status_changed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='status_changed_by')

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"      
