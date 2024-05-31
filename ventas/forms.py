from django.forms import ModelForm
from .models import Product, Supplier, Brand, Category
from django import forms


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'price', 'stock', 'brand', 'categories',
                  'line', 'supplier', 'expiration_date', 'image', 'state','user']
         


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'ruc', 'address', 'phone','user','image', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_ruc'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_phone'}),
            'user': forms.Select(attrs={'class': 'form-select', 'id': 'id_user'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'id_image'}),
            'state': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_state'}),
        }
    


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['description', 'user', 'state']
        
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'user', 'state']