from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = 'auth_user'

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    email = models.EmailField(
        verbose_name=_("email address"), unique=True,
        error_messages={
            'unique': _(
                "A user is already registered with this email address"),
        },
    )
    first_name = models.CharField(
        max_length=30, verbose_name=_("first name"), blank=True,
    )
    last_name = models.CharField(
        max_length=30, verbose_name=_("last name"), blank=True,
    )
    phone_number = models.CharField(max_length=30, verbose_name=_("phone number"), blank=True
                                    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"), default=timezone.now,
    )

    user_country = models.CharField(max_length=255)

    objects = UserManager()


class User_Account(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    default_date = models.CharField(max_length=10, blank=True, null=True)
    default_currency = models.CharField(max_length=3, blank=True, null=True)


    date_creation = models.DateTimeField(
        verbose_name=_("date_creation"), default=timezone.now,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User Account'
        verbose_name_plural = 'Users Accounts'


class Countries(models.Model):
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class DateFormat(models.Model):
    format = models.CharField(max_length=10)


    def __str__(self):
        return self.format


    class Meta:
        verbose_name = 'Format'
        verbose_name_plural = 'Formats'
