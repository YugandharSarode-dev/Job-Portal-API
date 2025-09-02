from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.contrib.auth.models import PermissionsMixin
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('mobile', username)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=256, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=256, blank=True, null=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    mobile = models.CharField(_('mobile'), max_length=16, null=True, blank=True, db_index=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        null=True,
        blank=True,
        unique=True
    )

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    STATUS_CHOICES = ((1, 'active'), (2, 'inactive'), (3, 'deleted'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    GROUP_CHOICES = [
        (1, 'superuser'),
        (2, 'employer'),
        (3, 'job_seeker')
    ]
    role = models.PositiveSmallIntegerField(choices=GROUP_CHOICES, default=2)

    created_by = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    login_otp = models.CharField(max_length=10, blank=True, null=True)
    login_otp_time = models.DateTimeField(blank=True, null=True)
    otp = models.CharField(max_length=20, blank=True, null=True)
    otp_time = models.DateTimeField(blank=True, null=True)
    new_otp = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

