from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Company, Supplier, Brand, Category
from .forms import ProductForm, SupplierForm, BrandForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def home(request):
    company = Company.objects.first()
    data = {
        'company': company,
    }
    return render(request, 'ventas/home.html', data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'ventas/signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 and password2 and password1 == password2:
                try:
                    user = User.objects.create_user(username=request.POST['username'], password=password1)
                    user.save()
                    login(request, user)
                    return render(request, 'ventas/signin.html')
                except IntegrityError:
                    return render(request, 'ventas/signup.html', {
                        'form': UserCreationForm(),
                        'error_message': 'Username already exists'
                    })
            else:
                return render(request, 'ventas/signup.html', {
                    'form': UserCreationForm(),
                    'error_message': 'Passwords do not match'
                })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'ventas/signin.html', {
            'form': AuthenticationForm()
        })
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ventas:products')
        else:
            return render(request, 'ventas/signin.html', {
                'form': AuthenticationForm,
                'error_message': 'Username or password is incorrect.'
            })
@login_required
def products(request):
    company = Company.objects.first()
    products = Product.objects.all().order_by('id','state')
    brands = Brand.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.filter(state=True)   # Filtrar proveedores activos
    users = User.objects.all()
    status_choices = Product.Status.choices
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            products = products.filter(description__icontains=query)
            
        data = {
            "title1": "Productos",
            "title2": "Consulta De Productos",
            'form': ProductForm(),
            'products': products,
            'company': company,
            'brands': brands,
            'categories': categories,
            'suppliers': suppliers,
            'users': users,
            'status_choices': status_choices,
        }
        return render(request, 'ventas/products/products.html', data)
    
    elif request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            if Product.objects.filter(description=description).exists():
                messages.error(request, f'El producto con la descripción "{description}" ya existe.')
                data = {
                    'form': form,  # Enviar el formulario con errores
                    'title1': "Productos",
                    'title2': "Consulta De Productos",
                    'products': products,
                    'company': company,
                    'brands': brands,
                    'categories': categories,
                    'suppliers': suppliers,
                    'users': users,
                    'status_choices': status_choices,
                }
                return render(request, 'ventas/products/products.html', data)
            else:
                form.save()
                return redirect('ventas:products')
        else:
            data = {
                'form': form,  # Enviar el formulario con errores
                'error_message': form.errors,
                'title1': "Productos",
                'title2': "Consulta De Productos",
                'products': products,
                'company': company,
                'brands': brands,
                'categories': categories,
                'suppliers': suppliers,
                'users': users,
                'status_choices': status_choices,
            }
            return render(request, 'ventas/products/products.html', data)

@login_required
def view_product(request, product_id):
    company = Company.objects.first()
    product = get_object_or_404(Product, id=product_id)  # Fetch the specific product or return 404
    brands = Brand.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    users = User.objects.all()
    status_choices = Product.Status.choices
     
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            # Optionally filter related products based on the query
            related_products = Product.objects.filter(description__icontains=query).exclude(id=product_id)
        else:
            related_products = None

        return render(request, 'ventas/products/view_product.html', {
            'title1': "Producto",
            'title2': "Visualizar De Producto",
            'form': ProductForm(),
            'product': product,  # Pass the single product to the template
            'related_products': related_products,  # Pass related products if any
            'company': company,
            'brands': brands,
            'categories': categories,
            'suppliers': suppliers,
            'users': users,
            'status_choices': status_choices,
        })
@login_required
def update_product(request, product_id):
    company = Company.objects.first()
    product = get_object_or_404(Product, pk=product_id)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    users = User.objects.all()
    status_choices = Product.Status.choices

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            description = form.cleaned_data['description']
            if Product.objects.filter(description=description).exclude(pk=product_id).exists():
                messages.error(request, f'El producto con la descripción "{description}" ya existe.')
            else:
                form.save()
                return redirect('ventas:products')
        error_message = form.errors
    else:
        form = ProductForm(instance=product)
        error_message = None

    selected_categories = product.categories.values_list('id', flat=True)
    data = {
        'form': form,
        "title1": "Productos",
        "title2": "Update Productos",
        'product': product,
        'company': company,
        'brands': brands,
        'categories': categories,
        'suppliers': suppliers,
        'users': users,
        'status_choices': status_choices,
        'selected_categories': selected_categories,
        'error_message': error_message,
    }
    return render(request, 'ventas/products/update_product.html', data)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    company = Company.objects.first()
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('ventas:products')
    
    return render(request, 'ventas/products/delete_product.html', {
        'title1': "Products",
        'title2': "Delete Productos",
        'product': product,
        'company': company,
    })
    
@login_required
def suppliers(request):
    company = Company.objects.first()
    suppliers = Supplier.objects.all().order_by('id')
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            suppliers = suppliers.filter(ruc__icontains=query)
        data = {
            "title1": "Suppliers",
            "title2": "Consulta De Suppliers",
            "form": SupplierForm(),
            'suppliers': suppliers,
            'company': company,
        }
        return render(request, 'ventas/suppliers/suppliers.html', data)
    
    elif request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            ruc = form.cleaned_data.get('ruc')
            if Supplier.objects.filter(ruc=ruc).exists():
                form.add_error('ruc', 'El proveedor con este RUC ya existe.')
                data = {
                    'form': form,  # Enviar el formulario con errores
                    'error_message': 'El proveedor con este RUC ya existe.',
                    "title1": "Suppliers",
                    "title2": "Consulta De Suppliers",
                    'suppliers': suppliers,
                    'company': company,
                }
                return render(request, 'ventas/suppliers/suppliers.html', data)
            else:
                form.save()
                return redirect('ventas:suppliers')
        else:
            print(form.errors)  # Añadir esto para ver errores en la consola
            data = {
                'form': form,  # Enviar el formulario con errores
                'error_message': form.errors,
                "title1": "Suppliers",
                "title2": "Consulta De Suppliers",
                'suppliers': suppliers,
                'company': company,
            }
            return render(request, 'ventas/suppliers/suppliers.html', data)
@login_required
def update_supplier(request, supplier_id):
    company = Company.objects.first()
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        
        if form.is_valid():
            ruc = form.cleaned_data.get('ruc')
            if Supplier.objects.filter(ruc=ruc).exclude(pk=supplier.pk).exists():
                form.add_error('ruc', 'El proveedor con este RUC ya existe.')
        
        if form.is_valid():  # Se llama a form.is_valid() nuevamente para evitar que se guarde con errores
            form.save()
            return redirect('ventas:suppliers')
        else:
            return render(request, 'ventas/suppliers/update_supplier.html', {
                'form': form,
                'error_message': form.errors,
                'title1': "Suppliers",
                'title2': "Update Suppliers",
                'supplier': supplier,
                'company': company,
            })
    else:
        form = SupplierForm(instance=supplier)
        data = {
            'form': form,
            "title1": "Suppliers",
            "title2": "Update Suppliers",
            'supplier': supplier,
            'company': company,
        }
        return render(request, 'ventas/suppliers/update_supplier.html', data)


@login_required
def delete_supplier(request, supplier_id):
    company = Company.objects.first()
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('ventas:suppliers')
    
    return render(request, 'ventas/suppliers/delete_supplier.html', {
        'title1': "Suppliers",
        'title2': "Eliminacion De Suppliers",
        'supplier': supplier,
        'company': company,
    })

@login_required
def view_supplier(request, supplier_id):
    company = Company.objects.first()
    supplier = get_object_or_404(Supplier, id=supplier_id)  # Fetch the specific supplier or return 404
    related_products = Product.objects.filter(supplier=supplier)  # Fetch products related to this supplier
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            # Optionally filter related suppliers based on the query
            similar_suppliers = Supplier.objects.filter(name__icontains=query).exclude(id=supplier_id)
        else:
            similar_suppliers = None

        return render(request, 'ventas/suppliers/view_supplier.html', {
            'title1': "Supplier",
            'title2': "View Supplier Details",
            'form': SupplierForm(instance=supplier),
            'supplier': supplier,  # Pass the single supplier to the template
            'related_products': related_products,  # Pass related products if any
            'similar_suppliers': similar_suppliers,  # Pass similar suppliers if any
            'company': company,
        })
@login_required
def brands(request):
    company = Company.objects.first()
    brands = Brand.objects.all().order_by('id')
    users = User.objects.all()
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            brands = brands.filter(id__icontains=query)
        data = {
            "title1": "Brands",
            "title2": "Brands Query",
            "form": BrandForm(),
            'brands': brands,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/brands/brands.html', data)
    elif request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            if Brand.objects.filter(description=description).exists():
                form.add_error('description', 'La marca con esta descripción ya existe.')
            else:
                form.save()
                return redirect('ventas:brands')
        
        # Si el formulario no es válido o si existe un duplicado, se regresa al template con errores
        data = {
            'form': form,  # Pasar el formulario con errores de vuelta al template
            'error_message': form.errors,  # Incluir mensajes de error si es necesario
            "title1": "Brands",
            "title2": "Brands Query",
            'brands': brands,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/brands/brands.html', data)


@login_required
def update_brand(request, brand_id):
    company = Company.objects.first()
    brand = get_object_or_404(Brand, pk=brand_id)
    users = User.objects.all()
    
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            # Verifica si ya existe otra marca con la misma descripción
            if Brand.objects.filter(description=description).exclude(pk=brand_id).exists():
                form.add_error('description', 'La marca con esta descripción ya existe.')
            else:
                form.save()
                return redirect('ventas:brands')
        
        # Si el formulario no es válido o si existe un duplicado, se regresa al template con errores
        return render(request, 'ventas/brands/update_brand.html', {
            'form': form,
            'error_message': form.errors,
            'title1': "Brands",
            'title2': "Update Brands",
            'brand': brand,
            'company': company,
            'users': users,
        })
    else:
        form = BrandForm(instance=brand)
        data = {
            'form': form,
            'title1': "Brands",
            'title2': "Update Brands",
            'brand': brand,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/brands/update_brand.html', data)


@login_required
def delete_brand(request, brand_id):
    company = Company.objects.first()
    brand = get_object_or_404(Brand, pk=brand_id)
    
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand deleted successfully!')
        return redirect('ventas:brands')
    
    return render(request, 'ventas/brands/delete_brand.html', {
        'title1': "Brands",
        'title2': "Delete Brands",
        'brand': brand,
        'company': company,
    })

@login_required
def categories(request):
    company = Company.objects.first()
    categories = Category.objects.all().order_by('id')
    users = User.objects.all()
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            categories = categories.filter(description__icontains=query)
        data = {
            "title1": "Categories",
            "title2": "Categories Query",
            "form": CategoryForm(),
            'categories': categories,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/categories/categories.html', data)
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            if Category.objects.filter(description=description).exists():
                form.add_error('description', 'La Categoria con esta descripción ya existe.')
            else:
                form.save()
                return redirect('ventas:categories')
        data={
                'form': form,  # Enviar el formulario con errores
                'error_message': form.errors,
                "title1": "Categories",
                "title2": "Categories Query",
                'categories': categories,
                'company': company,
                'users': users,
        }
        return render(request, 'ventas/categories/categories.html', data)

@login_required
def update_category(request, category_id):
    company = Company.objects.first()
    category = get_object_or_404(Category, pk=category_id)
    users = User.objects.all()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            # Verifica si ya existe otra marca con la misma descripción
            if Category.objects.filter(description=description).exclude(pk=category_id).exists():
                form.add_error('description', 'La marca con esta descripción ya existe.')
            
            else:
                form.save()
                return redirect('ventas:categories')
        return render(request, 'ventas/categories/update_category.html', {
            'form': CategoryForm(),
            'error_message': form.errors,
            'title1': "Categories",
            'title2': "Update Categories",
            'category': category,
            'company': company,
            'users': users,
        })
    else:
        form = CategoryForm(instance=category)
        data = {
            'form': form,
            "title1": "Categories",
            "title2": "Update Categories",
            'category': category,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/categories/update_category.html', data)

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    company = Company.objects.first()
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('ventas:categories')
    
    return render(request, 'ventas/categories/delete_category.html', {
        'title1': "Categories",
        'title2': "Delete Categories",
        'category': category,
        'company': company,
    })

