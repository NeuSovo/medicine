from django.contrib import admin

# Register your models here.
import re
from .models import *
from django.db import transaction


class NeiJIngBlankInline(admin.StackedInline):
    model = NeiJingParaGraph
    can_delete = False
    template = 'admin/stacked.html'
    readonly_fields = ('content', 'blank_index')

    def get_max_num(self, request, obj=None, **kwargs):
        """Hook for customizing the max number of extra inline forms."""
        return len(obj.paragraph.all())


@admin.register(NeiJingRaw)
class NeiJingRawAdmin(admin.ModelAdmin):
    '''Admin View for NeiJingRaw'''

    list_display = ('title',)
    # list_filter = ('',)
    inlines = [
        NeiJIngBlankInline,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = ('raw',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        else:
            return ('raw',)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        rs = re.compile(r'\w+\(.*?\)\w+[，,：;；:？?。]|\w+[，,：;；:？?。、]')
        blanks = []
        if change:
            print (1)
            return obj.save()

        try:
            with transaction.atomic():
                obj.save()
                for i in obj.raw.split('\n'):
                    if i=='':
                        break
                    blanks.append(NeiJingParaGraph(raw=obj, content=rs.findall(i)))
                NeiJingParaGraph.objects.bulk_create(blanks)
        except Exception as e:
            raise e

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            self.inlines = []
        else:
            self.inlines = [NeiJIngBlankInline]
        return super(NeiJingRawAdmin, self).get_inline_instances(request, obj)

