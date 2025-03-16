from django import forms
from .models import Requisition, RequisitionItem
from inventory.models import Brand

class RequisitionItemForm(forms.ModelForm):
    class Meta:
        model = RequisitionItem
        fields = ['item_requested', 'reason', 'quantity', 'brand']
        widgets = {
            'item_requested': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reason for request'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Enter quantity'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
        }

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = []  # Exclude 'requested_by' since the view handles it automatically

    def __init__(self, *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs)

# Define the formset with extra=1 to show one empty form initially
# can_delete=True allows users to delete items
RequisitionItemFormSet = forms.inlineformset_factory(
    Requisition, 
    RequisitionItem, 
    form=RequisitionItemForm, 
    extra=1, 
    can_delete=True
)
class RequisitionEditForm(forms.ModelForm):
    """Form for editing requisition properties like status"""
    class Meta:
        model = Requisition
        fields = ['status']  # Only allow editing status, not requested_by
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RequisitionEditForm, self).__init__(*args, **kwargs)
        
        # Only show status field for owners/admins
        if user and user.role != 'owner' and not user.is_superuser:
            self.fields['status'].widget.attrs['disabled'] = True
            self.fields['status'].widget.attrs['readonly'] = True

class RequisitionApprovalForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }