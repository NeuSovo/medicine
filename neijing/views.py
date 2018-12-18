import json
import random
from user.auth import login_required

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View, DetailView
from dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin

from .models import *


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

    @login_required
    def get(self, request, *args, **kwargs):
        exam_raw = get_object_or_404(self.model, pk=kwargs.get('pk'))
        exam_b, blanks= exam_raw.get_all_blank_count()
        exam = NeiJingExam(exam_raw=exam_raw, create_user=request.wuser, blanks=blanks)
        exam.save()
        return self.render_to_response({'msg': 'ok', 'exam_id': exam.id, 'total_blank': len(blanks), 'begin_time': exam.begin_time, 'raw': exam_b})

    @login_required
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


class ExamDetailView(JsonResponseMixin, DetailView):
    model = NeiJingExam
    foreign = False
    many = False
    pk_url_kwarg = 'pk'
    exclude_attr = ('blanks', 'u_answers', 'create_user_id', 'exam_raw_id')

    def get_context_data(self, **kwargs):
        context = super(ExamDetailView, self).get_context_data(**kwargs)
        if self.object.u_answers == "":
            context['res'] = "未完成"
        else:
            context['res'] = self.object.get_res()
        return context