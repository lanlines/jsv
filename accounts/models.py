from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    OWNER = 'owner'
    WAREHOUSE_MANAGER = 'warehouse_manager'
    SHOP_ATTENDANT = 'shop_attendant'
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (WAREHOUSE_MANAGER, 'Warehouse Manager'),
        (SHOP_ATTENDANT, 'Shop Attendant'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    def __str__(self):
        return self.username
    
    def is_owner(user): # fucntion to check if user is owner or superuser
        return user.is_authenticated and (user.role == 'owner' or user.is_superuser)
    