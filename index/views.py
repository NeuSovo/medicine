from django.shortcuts import render
from .models import *
from dss.Serializer import serializer
from django.http import JsonResponse
from dss.Mixin import MultipleJsonResponseMixin
from django.views.generic import ListView


def get_lunbo_img(request):
    count = request.GET.get('count')
    count = int(count) if count else 3
    lists = LunBo.objects.all()[:count]
    if lists:
        return JsonResponse({'list': serializer(lists)})
    return JsonResponse({})


class IndexList(MultipleJsonResponseMixin, ListView):
    model = Index
    query_set = Index.objects.all()
    paginate_by = 15
    datetime_type = 'string'
