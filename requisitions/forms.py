from django import forms
from .models import Requisition



class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['item_requested', 'reason', 'quantity']
        widgets = {
            'item_requested': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reason for request'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Enter quantity'}),
        }

class RequisitionEditForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['item_requested', 'reason', 'quantity']
        widgets = {
            'item_requested': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }