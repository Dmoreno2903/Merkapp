from django.contrib import admin
from .models import Supermercado, Mercado, Tipo

# Register your models here.
admin.site.register(Supermercado)
admin.site.register(Mercado)
admin.site.register(Tipo)