from django import forms
from .models import OrderJob

class OrderJobForm(forms.ModelForm):
    class Meta:
        model = OrderJob
        fields = ['nombre_cliente', 'numberPhone', 'dateOT', 'productList', 'typeService', 'paymentMethod']





