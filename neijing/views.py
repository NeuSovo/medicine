from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from django.views.generic import View, ListView
from .models import *
import random
import json


def match_answer(request, pid, iid):
    if not request.user.is_superuser:
        return JsonResponse({"msg": 'get out'})

    p = get_object_or_404(NeiJingParaGraph, pk=pid)
    blanks = p.blanks
    if iid in blanks:
        blanks.remove(iid)
        status = False
    else:
        status = True
        blanks.append(iid)

    p.blank_index = ','.join(map(str,blanks))
    p.save()
    return JsonResponse({'status': status})


class ExamView(JsonResponseMixin, View):
    model = NeiJingRaw

    def get(self, request, *args, **kwargs):
        exam_raw = get_object_or_404(self.model, pk=kwargs.get('pk'))
        exam_a, exam_b, blanks= exam_raw.get_all_blank_count()
        exam = NeiJingExam(exam_raw=exam_raw, blanks=blanks, right_answers=exam_a)
        exam.save()
        return self.render_to_response({'msg': 'ok', 'exam_id': exam.id, 'begin_time': exam.begin_time, 'raw': exam_b})


    def post(self, request, *args, **kwargs):
        exam = get_object_or_404(NeiJingExam, pk=kwargs.get('pk'))

        try:
            body = json.loads(request.body)
        except Exception as e:
            return self.render_to_response({'msg': 'error'})

        exam.u_answers = body
        exam.save()
        res = exam.get_res()

        return self.render_to_response({'msg': 'ok',
        'total_blank_count': len(exam.u_answers),
        'right_answer_count': exam.right_answer_count, 'res':res})


class NeiJingList(MultipleJsonResponseMixin, ListView):
    model = NeiJingRaw
    paginate_by = 20
    datetime_type = 'string'
    exclude_attr = ('raw',)
