
# django and drf lib
from django.db import transaction
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter

# models and serializers
from apis.user.models import User

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        '''
        ### AccountAdapter - save_user
        - adapter pattern으로 user를 실제로 만들어 주는 부분
        - 이 부분이 정의한 model과 core와 상이하면 login 할 때 vaildation 이 안됌
        '''
        data = form.cleaned_data
        user.email = data.get('email')
        user.name = data.get('name')
        user.set_password(data["password"])
        self.populate_username(request, user)
        user.save()
        return user