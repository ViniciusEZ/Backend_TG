from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):    
    name = models.CharField(null=True, max_length=128)
    email = models.EmailField(_('email address'), unique=True)
    
    password = models.CharField(_('password'), max_length=128)
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    
    # Custom Fields
    
    # first_name = models.CharField(_('first_name'), max_length=150, blank=True)
    # last_name = models.CharField(_('last_name'), max_length=150, blank=True)
    
    
    # Django stuff
    
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