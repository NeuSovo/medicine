from django.contrib import admin

from .models import *

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('disease_name',)
    filter_horizontal = ('main_symptoms', 'main_prescription')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


@admin.register(DiseaseType)
class DiseaseTypeAdmin(admin.ModelAdmin):
    '''Admin View for DiseaseType'''

    list_display = ('disease' ,'type_name',)

    filter_horizontal = ('add_prescription',)

admin.site.register(MainSymptoms)
admin.site.register(MainPrescription)
