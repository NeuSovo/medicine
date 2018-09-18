from django.views.generic import CreateView, View
from dss.Mixin import JsonResponseMixin

from .models import *
from .auth import UserWrap


class RegUserView(JsonResponseMixin, CreateView, UserWrap):
    model = User

    def post(self, request, *args, **kwargs) -> dict:
        self.check()
        if self.msg:
            return self.render_to_response({'msg': self.msg})

        if self.check_user_reg():
            token = self.gen_token(self.user)
            self.update_profile()
            # user = serializer(self.user)
            return self.render_to_response({'msg': 'success', 'user_obj': self.user, 'token': token})
        else:
            user, token = self.reg_user()
            return self.render_to_response({'msg': 'success', 'user_obj': user, 'token': token})


class LoginUserView(JsonResponseMixin, View):
    model = User

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not isinstance(request.wuser, self.model):
            return self.render_to_response({'msg': 'token 错误或过期'})

        return self.render_to_response({'msg': 'success', 'user_obj': request.wuser})
