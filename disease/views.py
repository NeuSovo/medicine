import json
from django.views.generic import CreateView, ListView, View
from dss.Mixin import JsonResponseMixin

from .apps import CAN_SUBMIT_LIMIT
from .models import *


class DiseaseView(JsonResponseMixin, View):
    model = Disease
    
    def get(self, request, *args, **kwargs):
        # TODO: 规则
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
                if matched >=  CAN_SUBMIT_LIMIT:
                    can_submit = True
                next_symptoms = next_symptoms.union(i.main_symptoms.all())

        next_symptoms = next_symptoms.difference(Symptoms.objects.filter(id__in=symptoms))

        return self.render_to_response({'can_submit': can_submit, 'next_symptoms': next_symptoms})
