from django.contrib import admin

# Register your models here.

from .models import Product, Variation, Test

admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(Test)
