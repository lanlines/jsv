from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from purchasing.models import Purchase, PurchaseItem, Supplier
from requisitions.models import Requisition
from .forms import SupplierEditForm, SupplierForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction




# Create your views here.
@login_required(login_url='login_view')
def supplier_view(request):
    if request.user.is_superuser or request.user.role == 'owner':    # only owner or superuser can view suppliers
        suppliers = Supplier.objects.all()
    else:
        raise PermissionDenied
    if request.method == 'POST':
        if 'add_supplier' in request.POST:
            form = SupplierForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Supplier created successfully.')
                return redirect('supplier')
            else:
                messages.error(request, 'Failed to create requisiiton. Please correct the errors below.')

        elif 'delete_supplier' in request.POST:
            supplier_id = request.POST.get('supplier_id')
            supplier = get_object_or_404(Supplier, pk=supplier_id)
            supplier.delete()
            messages.success(request, 'Supplier deleted successfully.')
            return redirect('supplier') 
        
        elif 'edit_supplier' in request.POST:
            supplier_id = request.POST.get('supplier_id')
            supplier = get_object_or_404(Supplier, pk=supplier_id)
            form = SupplierEditForm(request.POST, instance=supplier)
            if form.is_valid():
                form.save()
                messages.success(request, 'Supplier updated successfully.')
                return redirect('supplier')
            else:
                messages.error(request, 'Failed to update supplier. Please correct the errors below.')
        else:
            form = SupplierForm(request.POST)
    else:
        form = SupplierForm()
    return render(request, 'purchasing/supplier.html', {'suppliers': suppliers, 'form': form})

@login_required(login_url='login_view')
def purchase_view(request):
    if not (request.user.is_superuser or request.user.role in ['owner', 'purchasing_manager', 'purchasing_staff']):
        raise PermissionDenied
    
    # Get approved requisitions
    requisitions = Requisition.objects.prefetch_related('items').filter(status='approved' or 'purchased')
    if request.method == 'POST' and 'purchase_requisition' in request.POST:
        requisition_id = request.POST.get('requisition_id')
        requisition = get_object_or_404(Requisition, pk=requisition_id)
        supplier_id = request.POST.get('supplier')
        purchase_date = request.POST.get('purchase_date')
        notes = request.POST.get('notes')
        
        try:
            with transaction.atomic():
                # 1. Create a new Purchase record
                purchase = Purchase.objects.create(
                    requisition=requisition,
                    supplier_id=supplier_id,
                    purchase_date=purchase_date,
                    notes=notes,
                    grand_total=request.POST.get('grand_total', 0)
                )
                
                # 2. Create PurchaseItems for each item
                for item in requisition.items.all():
                    purchase_qty = int(request.POST.get(f'purchase_qty_{item.id}', 0))
                    unit_price = float(request.POST.get(f'unit_price_{item.id}', 0))
                    brand_id = request.POST.get(f'brand_{item.id}', None)
                    
                    if purchase_qty > 0 and unit_price > 0:
                            # set brand to None if not selected
                        brand = None
                        if brand_id and brand_id.strip():
                            try:
                                from inventory.models import Brand
                                brand = Brand.objects.get(pk=brand_id)
                            except (ImportError, Brand.DoesNotExist):
                                brand = None
                        PurchaseItem.objects.create(
                            purchase=purchase,
                            item=item.item_requested,
                            quantity=purchase_qty,
                            unit_price=unit_price,
                            total_price=purchase_qty * unit_price,
                            brand=brand
                        )
                
                # 3. Update the requisition status to "purchased"
                requisition.status = 'purchased'
                requisition.status_changed_by = request.user.role
                requisition.save()
                
                messages.success(request, f'Purchase successfully created for Requisition #{requisition_id}')
                
                
        except Exception as e:
            messages.error(request, f'Error processing purchase: {str(e)}')

    # Handle direct purchases (not tied to requisitions)
    elif request.method == 'POST' and 'add_direct_purchase' in request.POST:
        supplier_id = request.POST.get('supplier')
        purchase_date = request.POST.get('purchase_date')
        notes = request.POST.get('notes')
        grand_total = request.POST.get('grand_total', 0)
        
        try:
            with transaction.atomic():
                # 1. Create a new direct Purchase record (no requisition)
                purchase = Purchase.objects.create(
                    supplier_id=supplier_id,
                    purchase_date=purchase_date,
                    notes=notes,
                    grand_total=grand_total,
                )
                
                # 2. Get the number of items from the hidden field
                item_count = int(request.POST.get('item_count', 1))
                
                # 3. Process each item from the form
                for i in range(item_count):
                    item_name = request.POST.get(f'item_name_{i}')
                    purchase_qty = request.POST.get(f'purchase_qty_{i}')
                    unit_price = request.POST.get(f'unit_price_{i}')
                    brand_id = request.POST.get(f'brand_{i}')
                    
                    # Skip empty rows (user might have added and removed rows)
                    if not item_name or not purchase_qty or not unit_price:
                        continue
                    
                    purchase_qty = int(purchase_qty)
                    unit_price = float(unit_price)
                    
                    if purchase_qty > 0 and unit_price > 0:
                        # Get or create brand if specified
                        brand = None
                        if brand_id and brand_id.strip():
                            try:
                                from inventory.models import Brand
                                brand = Brand.objects.get(pk=brand_id)
                            except (ImportError, Brand.DoesNotExist):
                                brand = None
                        
                        # Create purchase item directly (no requisition item)
                        PurchaseItem.objects.create(
                            purchase=purchase,
                            item=item_name,  # Save item name directly
                            quantity=purchase_qty,
                            unit_price=unit_price,
                            total_price=purchase_qty * unit_price,
                            brand=brand
                        )
                
                messages.success(request, f'Direct purchase #{purchase.id} created successfully')
                
        except Exception as e:
            messages.error(request, f'Error processing direct purchase: {str(e)}')
    
    # Rest of your view code...
    try:
        from inventory.models import Brand
        brands = Brand.objects.all()
    except:
        brands = None

    context = {
        'requisitions': requisitions, 
        'suppliers': Supplier.objects.all(),
    }
    
    if brands:
        context['brands'] = brands
    return render(request, 'purchasing/purchase.html', context)

@login_required(login_url='login_view')
def purchase_list_view(request):
    if not (request.user.is_superuser or request.user.role in ['owner', 'purchasing_manager', 'purchasing_staff']):
        raise PermissionDenied
    
    context = {
        'purchases': Purchase.objects.prefetch_related('items').select_related('supplier', 'requisition').all()
    }
    return render(request, 'purchasing/purchase_list.html', context)





# ///////////////////     fix purchase list to display only purchsaes list