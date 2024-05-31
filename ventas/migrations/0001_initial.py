# Generated by Django 4.2 on 2024-05-28 00:14

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djangoCrud.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Articulo')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, verbose_name='Activo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Categoria')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, verbose_name='Activo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(blank=True, max_length=13, null=True, unique=True, verbose_name='Dni')),
                ('first_name', models.CharField(max_length=50, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('gender', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=1, verbose_name='Sexo')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Fecha Nacimiento')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefono')),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='Correo')),
                ('image', models.ImageField(blank=True, default='products/default.png', null=True, upload_to='customers/', verbose_name='Foto')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, verbose_name='Activo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha Emision')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Subtotal')),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Iva')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='descuento')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Total')),
                ('payment', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Pago')),
                ('change', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Cambio')),
                ('status', models.CharField(choices=[('F', 'Factura'), ('A', 'Anulada'), ('D', 'Devolucion')], default='F', max_length=1, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, verbose_name='Activo')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_invoices', to='ventas.customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
                'ordering': ('-issue_date', 'customer'),
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ruc', models.CharField(max_length=13, validators=[djangoCrud.utils.valida_cedula])),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe contener entre 9 y 15 dígitos.', regex='^\\d{9,15}$')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, verbose_name='Activo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Articulo')),
                ('cost', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=10, verbose_name='Costo Producto')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=10, verbose_name='Precio')),
                ('stock', models.IntegerField(default=100, help_text='Stock debe estar en 0 y 10000 unidades', verbose_name='Stock')),
                ('iva', models.IntegerField(choices=[(0, '0%'), (5, '5%'), (15, '15%')], default=15, verbose_name='IVA')),
                ('expiration_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha Caducidad')),
                ('line', models.CharField(choices=[('RS', 'Rio Store'), ('FS', 'Ferrisariato'), ('CS', 'Comisariato')], default='CS', max_length=2, verbose_name='Linea')),
                ('image', models.ImageField(blank=True, default='products/default.png', null=True, upload_to='products/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, verbose_name='Activo')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='ventas.brand', verbose_name='Marca')),
                ('categories', models.ManyToManyField(to='ventas.category', verbose_name='Categoria')),
                ('supplier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ventas.supplier', verbose_name='Proveedor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Metodo Pago')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, verbose_name='Activo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Metodo de Pago',
                'verbose_name_plural': 'Metodo de Pagos',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=16, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='ventas.invoice', verbose_name='Factura')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Product', to='ventas.product', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Factura Detalle',
                'verbose_name_plural': 'Factura Detalles',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_invoices', to='ventas.paymentmethod', verbose_name='Metodo pago'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='supplier',
            index=models.Index(fields=['name'], name='ventas_supp_name_e27016_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['description'], name='ventas_prod_descrip_7e1610_idx'),
        ),
        migrations.AddIndex(
            model_name='invoicedetail',
            index=models.Index(fields=['id'], name='ventas_invo_id_18d5e5_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['issue_date'], name='ventas_invo_issue_d_85cb75_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['customer'], name='ventas_invo_custome_af10cd_idx'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name'], name='ventas_cust_last_na_91f51b_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['description'], name='ventas_cate_descrip_b58bd2_idx'),
        ),
        migrations.AddIndex(
            model_name='brand',
            index=models.Index(fields=['description'], name='ventas_bran_descrip_a2ee89_idx'),
        ),
    ]
