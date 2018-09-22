import json
from user.auth import login_required

from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, View
from dss.Mixin import JsonResponseMixin
from dss.Serializer import serializer

from .apps import CAN_SUBMIT_LIMIT
from .models import *


class DiseaseView(JsonResponseMixin, View):
    model = Disease
    
    @login_required
    def get(self, request, *args, **kwargs):
        # TODO: rules
        print (request.wuser)
        return self.render_to_response(Symptoms.objects.all())

    def post(self, request, *args, **kwargs):
        try:
            symptoms = json.loads(request.body)['symptoms']
        except Exception as e:
            return self.render_to_response({'msg': 'error'})

        next_symptoms = self.model.objects.none()
        can_submit = False
        for i in self.model.objects.all().iterator():
            matched = i.get_compatibility(symptoms)
            if matched > 0:
                # 可取列表里只有一个的优化
                if matched >=  CAN_SUBMIT_LIMIT: can_submit = True
                next_symptoms = next_symptoms.union(i.main_symptoms.all())

        next_symptoms = next_symptoms.difference(Symptoms.objects.filter(id__in=symptoms))

        return self.render_to_response({'can_submit': can_submit, 'next_symptoms': next_symptoms})


class DiseaseSubmit(JsonResponseMixin, View):
    model = Case

    def post(self, request, *args, **kwargs):
        if not isinstance(request.wuser, User):
            return self.render_to_response({'msg': 'token 错误或过期'})
        
        try:
            symptoms = json.loads(request.body)['symptoms']
        except Exception as e:
            return self.render_to_response({'msg': 'error'})

        max_disease = Disease()
        max_matched = 0
        # TODO: fixed result based on lens
        for i in Disease.objects.all().iterator():
            matched = i.get_compatibility(symptoms)
            if matched > max_matched:
                max_disease = i
                max_matched = matched

        case = self.model.create(create_user=request.wuser, case_disease=max_disease, symptoms=symptoms)

        if not (isinstance(case, self.model)):
            return self.render_to_response({'msg': case})
        
        typing = serializer(max_disease.diseasetyping_set.all(), exclude_attr=('disease',))

        return self.render_to_response({'matched': max_matched, 'case': case, 
                        'typing': typing})


class DiseaseResultView(JsonResponseMixin, View):
    model = Case
    
    def post(self, request, *args, **kwargs):
        if not isinstance(request.wuser, User):
            return self.render_to_response({'msg': 'token 错误或过期'})

        try:
            body = json.loads(request.body)
        except Exception as e:
            return self.render_to_response({'msg': 'error'})

        case = get_object_or_404(self.model, pk=body.get('case_id'))
        if case.create_user != request.wuser:
            return self.render_to_response({'msg': 'case_id 错误'})
        
        typings = body.get('typing')

        # 是不是没有分型
        if not isinstance(typings, list):
            return self.render_to_response({'msg': 'error'})

        case.create_typing(typings)

        result = case.get_result()
        return self.render_to_response({'case': case, 'result': result})
