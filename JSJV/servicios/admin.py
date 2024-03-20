from django.contrib import admin
from .models import OrderJob, ProductList, OutputOJ, Income, TypeService
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import OrderJob

from django.urls import reverse
from django.shortcuts import redirect


@admin.register(OrderJob)
class OrderJobAdmin(ImportExportModelAdmin):
    list_display = ('nombre_cliente','email_cliente','numberPhone', 'dateOT', 'get_product_amount', 'get_product_description' , 'paymentMethod','totalPrice',)
    list_display_links = ('dateOT',)  
    list_editable = ('totalPrice',)
    list_filter = ('dateOT',)
    list_per_page = 5
    exclude = ('totalPrice',) 
    actions = ['custom_button']

    def get_product_amount(self, obj):
        return obj.productList.amount if obj.productList else None
    get_product_amount.short_description = 'Cantidad Producto'

    def get_product_description(self, obj):
        return obj.productList.description if obj.productList else None
    get_product_description.short_description = 'Descripción Producto'

    def custom_button(self, request, queryset):
        url = reverse('PDFot')
        return redirect(url)

    custom_button.short_description = 'Descargar PDF'

@admin.register(ProductList)
class ProductListAdmin(ImportExportModelAdmin):
    list_display = ('amount', 'description', 'get_status', 'get_category')
    list_per_page = 5

    def get_status(self, obj):
            return obj.status

    get_status.short_status = 'Estados'

    def get_category(self, obj):
            return obj.category

    get_category.short_category = 'Categoria'


@admin.register(OutputOJ)
class OutputOJAdmin(ImportExportModelAdmin):
    list_display = ('id', 'dateOutput', 'amountOutputs')
    list_editable = ('amountOutputs',)
    list_per_page = 5

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('paymentMethod',)
    list_display_links = ('paymentMethod',)
    list_per_page = 5

@admin.register(TypeService)
class TypeServiceAdmin(admin.ModelAdmin):
    list_display = ('get_descriptionTS',)
    list_per_page = 5

    def get_descriptionTS(self, obj):
        return obj.descriptionTS

    get_descriptionTS.short_description = 'Servicio'




