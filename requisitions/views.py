from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
# from .models import Requisition
from django.contrib.auth.decorators import login_required

from requisitions.models import Requisition
from .forms import RequisitionForm
from django.contrib import messages

# Create your views here.

@login_required(login_url='login_view')
def requisitions_view(request):
    if request.user.role == 'owner' or request.user.role == 'warehouse_manager':    #owner &manager can view all requisitions
        reqiusitions = Requisition.objects.all()
    else:   #shop attendant can view only his/her requisitions
        reqiusitions = Requisition.objects.filter(requested_by=request.user.role)
    if request.method == 'POST':
        if 'edit_requisition' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            reqiusition = get_object_or_404(Requisition, pk=requisition_id)
            form = RequisitionForm(request.POST, instance=reqiusition)
            if form.is_valid():
                form.save()
                messages.success(request, 'Requisition updated successfully.')
                return redirect('requisitions')
            else:
                messages.error(request, 'Failed to update requisition. Please correct the errors below.')
        elif 'delete_requisition' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            reqiusition = get_object_or_404(Requisition, pk=requisition_id)
            reqiusition.delete()
            messages.success(request, 'Requisition deleted successfully.')
            return redirect('requisitions')
    else:
        form = RequisitionForm()
    return render(request, 'requisitions/requisitions.html', {'requisitions': reqiusitions, 'form': form})



@login_required(login_url='login_view')
def create_requisition_view(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            requisition = form.save(commit=False)
            requisition.requested_by = request.user.role
            requisition.save()
            messages.success(request, 'Requisition created successfully.')
            return redirect('create_requisition')  # Redirect to the same view to clear the form
        else:
            messages.error(request, 'Error creating requisition. Please correct the errors below.')
    else:
        form = RequisitionForm()
    return render(request, 'requisitions/create_requisition.html', {'form': form})

# def requisition_list(request):
#     requisitions = Requisition.objects.all()
#     return render(request, 'requisitions/requisition_list.html', {'requisitions': requisitions})

# def requisition_detail(request, pk):
#     requisition = Requisition.objects.get(pk=pk)
#     return render(request, 'requisitions/requisition_detail.html', {'requisition': requisition})