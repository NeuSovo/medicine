from django.contrib import admin

from .models import *

class DiseaseTypingSymptomsInline(admin.TabularInline):
    model = DiseaseTypingSymptoms


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('id', 'disease_name',)
    filter_horizontal = ('main_symptoms', 'main_prescription')
    ordering = ('id',)


@admin.register(DiseaseTyping)
class DiseaseTypeAdmin(admin.ModelAdmin):
    '''Admin View for DiseaseType'''

    list_display = ('disease' ,'type_name',)

    filter_horizontal = ('add_prescription',)

    inlines = [
        DiseaseTypingSymptomsInline,
    ]


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    '''Admin View for Case'''

    list_display = ('case_id', 'create_time', 'create_user', 'case_disease')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)

    ordering = ('-create_time',)


admin.site.register(Symptoms)
admin.site.register(Prescription)
