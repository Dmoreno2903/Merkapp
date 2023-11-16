from django.forms import ModelForm
from .models import Mercado

class MercadoForm(ModelForm):
    class Meta:
        model = Mercado
        fields = ['producto', 'costo', 'supermercado', 'tipo']
