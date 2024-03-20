from django.contrib import admin
from .models import Machine,Inventory,Input
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.shortcuts import redirect
from django.urls import reverse
@admin.register(Input)
class InputAdmin(ImportExportModelAdmin):
    list_display = ('product_type','amountI','supplier_nameI')
    


@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin):
   list_display = ('machine_type','amountM','supplier_nameM')
  



@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    list_display = ('get_product_amountI', 'get_product_supplier_nameI','get_product_amountM','get_product_supplier_nameM')
    list_per_page=2

    def get_product_supplier_nameI(self, obj):
        return obj.input.supplier_nameI if obj.input else None
    get_product_supplier_nameI.short_description = 'Proovedor Insumo'

    def get_product_amountI(self, obj):
        return obj.input.amountI if obj.input else None
    get_product_amountI.short_description = 'Cantidad insumos'

    def get_product_supplier_nameM(self, obj):
        return obj.machine.supplier_nameM if obj.machine else None
    get_product_supplier_nameM.short_description = 'Proovedor maquinas'

    def get_product_amountM(self, obj):
        return obj.machine.amountM if obj.machine else None
    get_product_amountM.short_description = 'Cantidad maquinas'



    actions = ['custom_button']

    def custom_button(self, request, queryset):

        url = reverse('PDFinve')
        return redirect(url)

    custom_button.short_description = 'Descargar PDF'
#admin.site.register(Machine)
#admin.site.register(Inventory)
#admin.site.register(Input)

