from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager

class User(AbstractBaseUser):    
    name = models.CharField(null=True, max_length=128)
    email = models.EmailField(_('email address'), unique=True)
    
    password = models.CharField(_('password'), max_length=128)
    phone_number = models.TextField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    objects = UserManager()
    
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        db_table = 'user"."user'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=128)
    numero = models.CharField(max_length=16)
    complemento = models.CharField(max_length=16)
    bairro = models.CharField(max_length=64)
    cidade = models.CharField(max_length=64)
    uf = models.CharField(max_length=2)

    class Meta:
        db_table = 'user"."address'    
