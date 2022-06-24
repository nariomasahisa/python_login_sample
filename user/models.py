from unicodedata import normalize
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, _user_has_perm
)
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class AccountManager(BaseUserManager):
    # ユーザの作成
    def create_user(self, request_data, **kwargs):
        now = timezone.now()
        if not request_data('email'):
            raise ValueError('Users must have an email address')
        
        profile = ''
        if request_data.get('profile'):
            profile = request_data('profile')

        user = self.model(
            username = request_data['username'],
            email = self.normalize_email(request_data['email']),
            id_active = True,
            last_login = now,
            date_joined = now,
            profile = profile
        )

        user.set_password(request_data['password'])
        user.save(using=self._db)
        return user