from django.contrib import admin
from .models import Product, Brand, Supplier, Category, Customer, PaymentMethod, Invoice, InvoiceDetail, Company

# Register your models here.
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(PaymentMethod)
admin.site.register(Invoice)
admin.site.register(InvoiceDetail)
admin.site.register(Company)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista de productos en el panel de administración
    list_display = ['description', 'price', 'stock', 'brand','supplier','line','categorias','state']
    # Define los campos por los cuales se pueden filtrar los productos en el panel de administración
    list_filter = ['state', 'brand','line']
    # Especifica los campos por los cuales se puede buscar productos en el panel de administración
    search_fields = ['description']
    # Define un filtro de jerarquía de fechas en el panel de administración para los productos
    date_hierarchy = 'expiration_date'
    # Define el orden en el que se muestran los productos en la lista del panel de administración
    ordering = ['description']

    # Define un método para mostrar las categorías de cada producto en la lista del panel de administración
    def categorias(self, obj):
        # Devuelve una cadena que contiene las descripciones de todas las categorías asociadas al producto, separadas por un guion (-)
        return " - ".join([c.description for c in obj.categories.all().order_by('description')])
