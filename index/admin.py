from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(LunBo)
class LunBoAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ('title',)
