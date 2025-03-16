from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
# from .models import Requisition
from django.contrib.auth.decorators import login_required

from requisitions.models import Requisition
from .forms import RequisitionForm, RequisitionItemFormSet, RequisitionEditForm
from django.contrib import messages
from django.db import transaction

# Create your views here.

# @login_required(login_url='login_view')
# def requisitions_view(request):
#     if request.user.role == 'owner' or request.user.role == 'warehouse_manager':    #owner &manager can view all requisitions
#         reqiusitions = Requisition.objects.all()
#     else:   #shop attendant can view only his/her requisitions
#         reqiusitions = Requisition.objects.filter(requested_by=request.user.role)
#     if request.method == 'POST':
#         if 'edit_requisition' in request.POST:
#             requisition_id = request.POST.get('requisition_id')
#             reqiusition = get_object_or_404(Requisition, pk=requisition_id)
#             form = RequisitionForm(request.POST, instance=reqiusition)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Requisition updated successfully.')
#                 return redirect('requisitions')
#             else:
#                 messages.error(request, 'Failed to update requisition. Please correct the errors below.')
#         elif 'delete_requisition' in request.POST:
#             requisition_id = request.POST.get('requisition_id')
#             reqiusition = get_object_or_404(Requisition, pk=requisition_id)
#             reqiusition.delete()
#             messages.success(request, 'Requisition deleted successfully.')
#             return redirect('requisitions')
#         elif 'reject_requisition' in request.POST:
#             requisition_id = request.POST.get('requisition_id')
#             reqiusition = get_object_or_404(Requisition, pk=requisition_id)
#             reqiusition.status = 'rejected'
#             reqiusition.save()
#             messages.success(request, 'Requisition rejected successfully.')
#             return redirect('requisitions')
#     else:
#         form = RequisitionForm()
#     return render(request, 'requisitions/requisitions.html', {'requisitions': reqiusitions, 'form': form})
@login_required(login_url='login_view')
def requisitions_view(request):
    if request.user.is_superuser or request.user.role == 'owner':  # only owner or superuser can view all requisitions
    # Use prefetch_related to efficiently load all related items in a single query
        requisitions = Requisition.objects.prefetch_related('items').all()
    else:
        # Filter by user role and prefetch related items
        requisitions = Requisition.objects.prefetch_related('items').filter(requested_by=request.user.role)

    if request.method == 'POST':
        if 'edit_requisition' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            requisition = get_object_or_404(Requisition, pk=requisition_id)
            
            # Ensure user has permission to edit this requisition
            if requisition.requested_by != request.user.role and not request.user.is_superuser and request.user.role != 'owner':
                messages.error(request, 'You do not have permission to edit this requisition.')
                return redirect('requisitions')
            
            # Only owners/superusers can change status
            if request.user.is_superuser or request.user.role == 'owner':
                form = RequisitionEditForm(request.POST, instance=requisition, user=request.user)
            else:
                form = RequisitionEditForm(instance=requisition, user=request.user)
            
            # Use the 'items' prefix to match the form fields in the modal
            formset = RequisitionItemFormSet(request.POST, instance=requisition, prefix='items')
            
            try:
                with transaction.atomic():
                    # For non-admins, we only validate the formset
                    if request.user.is_superuser or request.user.role == 'owner':
                        form_valid = form.is_valid()
                    else:
                        form_valid = True  # Skip form validation for regular users
                        
                    formset_valid = formset.is_valid()
                    
                    if form_valid and formset_valid:
                        # Only save the main form for admins/owners
                        if request.user.is_superuser or request.user.role == 'owner' and form_valid:
                            requisition = form.save(commit=False)
                            if 'status' in form.changed_data:
                                requisition.status_changed_by = request.user.role
                            requisition.save()
                        
                        # Save the formset (only updates existing items)
                        instances = formset.save(commit=False)
                        
                        # Save each item instance
                        for instance in instances:
                            instance.requisition = requisition
                            instance.save()
                        
                        messages.success(request, 'Requisition updated successfully.')
                        return redirect('requisitions')
                    else:
                        # Create detailed error messages
                        if not form_valid and (request.user.is_superuser or request.user.role == 'owner'):
                            for field, errors in form.errors.items():
                                for error in errors:
                                    messages.error(request, f"Error in {field}: {error}")
                                        
                        if not formset_valid:
                            for i, form_errors in enumerate(formset.errors):
                                if form_errors:
                                    for field, errors in form_errors.items():
                                        for error in errors:
                                            messages.error(request, f"Error in item #{i+1}, {field}: {error}")
                                            
                        messages.error(request, 'Failed to update requisition. Please correct the errors below.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        elif 'delete_requisition' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            requisition = get_object_or_404(Requisition, pk=requisition_id)
            requisition.delete()
            messages.success(request, 'Requisition deleted successfully.')
            return redirect('requisitions')
        elif 'approve_requisition' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            requisition = get_object_or_404(Requisition, pk=requisition_id)
            requisition.status = 'approved'
            requisition.status_changed_by = request.user.role
            requisition.save()
            messages.success(request, 'Requisition approved successfully.')
            return redirect('requisitions')
        elif 'reject_requisition' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            requisition = get_object_or_404(Requisition, pk=requisition_id)
            requisition.status = 'rejected'
            requisition.status_changed_by = request.user.role
            requisition.save()
            messages.success(request, 'Requisition rejected successfully.')
            return redirect('requisitions')
    else:
        form = RequisitionForm()
        formset = RequisitionItemFormSet()

    # Check if we have any brands for the form
    try:
        from inventory.models import Brand
        brands = Brand.objects.all()
    except:
        brands = None

    context = {
        'requisitions': requisitions, 
        'form': form, 
        'formset': formset
    }
    
    # Add brands to context if available
    if brands:
        context['brands'] = brands
        
    return render(request, 'requisitions/requisitions.html', context)

@login_required(login_url='login_view')
def create_requisition_view(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)  
        formset = RequisitionItemFormSet(request.POST, prefix='items')

        if form.is_valid() and formset.is_valid():
            requisition = form.save(commit=False)
            requisition.requested_by = request.user.role  # Automatically set from logged-in user's role
            requisition.save()

            formset.instance = requisition
            formset.save()

            messages.success(request, 'Requisition created successfully.')
            return redirect('create_requisition')
        else:
            messages.error(request, 'Error creating requisition. Please correct the errors below.')
    else:
        form = RequisitionForm()
        formset = RequisitionItemFormSet(prefix='items')

    return render(request, 'requisitions/create_requisition.html', {'form': form, 'formset': formset})

# def requisition_list(request):
#     requisitions = Requisition.objects.all()
#     return render(request, 'requisitions/requisition_list.html', {'requisitions': requisitions})

# def requisition_detail(request, pk):
#     requisition = Requisition.objects.get(pk=pk)
#     return render(request, 'requisitions/requisition_detail.html', {'requisition': requisition})