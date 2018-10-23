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

    exclude_attr = ('openid', 'reg_date', 'last_login', 'topic')

    def get(self, request, *args, **kwargs):
        disease = get_object_or_404(Disease, pk=kwargs.get('disease_id', 0))
        return self.render_to_response(disease.comment_set.all().order_by("comment_time"))

    @login_required
    def post(self, request, *args, **kwargs):
        disease = get_object_or_404(Disease, pk=kwargs.get('disease_id', 0))

        try:
            body = json.loads(request.body)
        except Exception as e:
            return self.render_to_response({'msg': str(e)})

        to_user = None
        if body.get('is_reply'):
            try:
                to_user = User.objects.get(pk=body.get('to_user_id', 0))
            except Exception as e:
                raise e
                return self.render_to_response({'msg': 'user_id not found'})
            # to_user = get_object_or_404(User, pk=body.get('to_user_id', 0))

        # TODO: to detail this content
        content = body.get('content')
        try:
            self.model.objects.create(topic=disease, content=content, from_user=request.wuser, to_user=to_user)
        except Exception as e:
            print(e)
            return self.render_to_response({'msg': str(e)})

        return self.render_to_response({'msg': 'ok'})
