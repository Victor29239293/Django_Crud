from django.urls import path

from ventas import views
from django.conf import settings
from django.conf.urls.static import static
 
app_name='ventas' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # urls de vistas 
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    
    path('products/', views.products, name='products'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('brands/', views.brands, name='brands'),
    path('categories/', views.categories, name='categories'),
    
    path('products/update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('products/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/view_product/<int:product_id>/', views.view_product, name='view_product'),
    
    path('suppliers/update_supplier/<int:supplier_id>/', views.update_supplier, name='update_supplier'),
    path('suppliers/delete_supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('suppliers/view_supplier/<int:supplier_id>/', views.view_supplier, name='view_supplier'),
    
    path('brands/update_brand/<int:brand_id>/', views.update_brand, name='update_brand'),
    path('brands/delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    
    path('categories/update_category/<int:category_id>/', views.update_category, name='update_category'),
    path('categories/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

