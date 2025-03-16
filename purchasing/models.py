from django.db import models
from requisitions.models import RequisitionItem, Requisition

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='requisition', blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier')
    purchase_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Purchase #{self.id} - {self.requisition}"
        
    class Meta:
        ordering = ['-purchase_date']

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    item = models.CharField(max_length=255)
    brand = models.ForeignKey('inventory.Brand', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.requisition_item.item_requested}"