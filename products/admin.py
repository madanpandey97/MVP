from django.contrib import admin
from products.models import Product, ProductView

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductView)
