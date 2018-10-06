import json
from user.auth import login_required
from dss.Mixin import JsonResponseMixin

from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, View

from .models import Comment
from disease.models import Disease
from user.models import User

class CommentView(JsonResponseMixin, View):
    model = Comment

    def get(self, request, *args, **kwargs):
        disease = get_object_or_404(Disease, pk=kwargs.get('disease_id', 0))


    @login_required
    def post(self, request, *args, **kwargs):
        disease = get_object_or_404(Disease, pk=kwargs.get('disease_id', 0))

        try:
            body = json.loads(request.body)
        except Exception as e:
            return self.render_to_response({'msg': 'error'})

        if body.get('is_reply'):
            to_user = get_object_or_404(User, pk=body.get('to_user'))

        self.model.create(topic=disease, )