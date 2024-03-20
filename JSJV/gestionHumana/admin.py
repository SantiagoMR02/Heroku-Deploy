from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from django.contrib import admin
from .models import Schedule, Salary,Activity
from django.urls import reverse
from django.shortcuts import redirect
# Register your models here.

@admin.register(Salary)
class Salary(ImportExportModelAdmin):
    list_display = ('detailSalary', 'nameEmploye','numberAccount','totalSalary','get_product_ActivityValue', 'schedules','amountActivity',)
    list_display_links=('get_product_ActivityValue', 'schedules',)
    list_editable=('numberAccount','totalSalary',)
    list_per_page=5
    exclude = ('totalSalary',) 
    actions = ['custom_button']

    def get_product_ActivityValue(self, obj):
        return obj.Activity.ActivityValue if obj.Activity else None
    get_product_ActivityValue.short_description = 'Valor de desarrollo'

    def custom_button(self, request, queryset):
        url = reverse('PDFsal')
        return redirect(url)

    custom_button.short_description = 'Descargar PDF'


@admin.register(Schedule)
class Schedule(admin.ModelAdmin):
    list_display = ('schedule',)
    list_per_page=5