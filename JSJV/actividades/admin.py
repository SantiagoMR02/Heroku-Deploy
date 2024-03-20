
from django.contrib import admin
from .models import Novelty,StateAc,Activity
from import_export import resources
from django.urls import reverse
from import_export.admin import ImportExportModelAdmin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.contrib import messages
from django import forms

@admin.register(Novelty)
class NoveltyAdmin(admin.ModelAdmin):
    list_display = ('dateN', 'get_states')

    def get_states(self, obj):
            return obj.stateN

    get_states.short_description = 'Estados'

@admin.register(StateAc)
class StateAcAdmin(admin.ModelAdmin):
   list_display = ('stateAc',)

@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin):
    list_display = ('dateAc', 'timeAc', 'get_novelty_state', 'stateAc', 'orderJob', 'input', 'machine', 'ActivityValue','amountToUse',)
    list_display_links = ('dateAc', 'orderJob',)
    list_editable = ('timeAc',)
    search_fields = ('dateAc',)
    list_filter = ('stateAc',)
    list_per_page = 5

    actions = ['custom_button']

    def get_novelty_state(self, obj):
        return obj.noveltyAc.stateN if obj.noveltyAc else None

    get_novelty_state.short_description = 'Novedad Actividad'

    def custom_button(self, request, queryset):
        url = reverse('PDFacti')
        return redirect(url)

    custom_button.short_description = 'Descargar PDF'

