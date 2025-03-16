from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from .models import Brand
from django.shortcuts import render, redirect
from .forms import BrandForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


# Create your views here.

@login_required(login_url='login_view')
def brand_view(request):
    brands = Brand.objects.all()
    if not (request.user.is_superuser or request.user.role in ['owner', 'purchasing_manager', 'purchasing_staff']):
        raise PermissionDenied
    if request.method == 'POST':
        if 'add_brand' in request.POST:
            name = request.POST.get('name')
            description = request.POST.get('description')
            Brand.objects.create(name=name, description=description)
            messages.success(request, 'Brand added successfully!')
            return redirect('brand')
            
        elif 'edit_brand' in request.POST:
            brand_id = request.POST.get('brand_id')
            brand = Brand.objects.get(id=brand_id)
            brand.name = request.POST.get('name')
            brand.description = request.POST.get('description')
            brand.save()
            messages.success(request, 'Brand updated successfully!')
            return redirect('brand')
            
        elif 'delete_brand' in request.POST:
            brand_id = request.POST.get('brand_id')
            Brand.objects.filter(id=brand_id).delete()
            messages.success(request, 'Brand deleted successfully!')
            return redirect('brand')

    else:
        form = BrandForm()
        context = {
        'brands': brands
        }

    return render(request, 'inventory/brand.html', context)
