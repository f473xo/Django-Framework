from pathlib import Path
from time import time

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _


# Функция динамического задания имени
def users_avatars_path(instance, filename):
    # file will be uploaded to
    # MEDIA_ROOT / user_<username> / avatars / <filename>
    num = int(time() * 1000)
    # расширение файла
    suff = Path(filename).suffix
    return "user_{0}/avatars/{1}".format(instance.username, f"pic_{num}{suff}")


"""
Что мы изменили в новой модели пользователя:
1. Валидатор для поля username. Валидаторы — это функции, которые проверяют содержимое
поля перед созданием записи в таблице БД. Теперь поле содержит только ASCII-символы.
2. Добавилось поле возраста — age.
3. Поле email теперь обязательно для заполнения и уникально.
4. Теперь есть поле avatar для загрузки фотографии пользователя.
"""


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Теперь поле содержит только ASCII-символы.
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. ASCII letters and digits only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists."), },
        )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    # Добавилось поле возраста — "age"
    age = models.PositiveIntegerField(blank=True, null=True)
    # еперь есть поле avatar для загрузки фотографии пользователя
    avatar = models.ImageField(upload_to=users_avatars_path, blank=True, null=True)
    # Расширяем свойства поля "email" - теперь обязательно для заполнения и уникально
    email = models.CharField(
        _("email address"),
        max_length=256,
        unique=True,
        error_messages={"unique": _("A user with that email address already exists."), },
        )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
        )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. \
            Unselect this instead of deleting accounts."),
        )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
