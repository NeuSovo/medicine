from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, View
from dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from dss.Serializer import serializer

from .models import *
from disease.models import Category


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


class BaikeView(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        res = []
        for i in Category.objects.all().iterator():
            res.append({
                'category': serializer(i),
                'disease': [{"id": j.id, "disease_name": j.disease_name} for j in i.disease_set.all()]
            })

        return JsonResponse(res, safe=False)
