from django.utils.timezone import now
from django.db import models, transaction
from django.contrib import admin
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

from users.managers import UserManager
from products.models import File


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    birthday = models.DateField(_('birthday'), null=True)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    @property
    @admin.display(
        ordering=_('last_name'),
        description=_('Full name of the user'),
    )
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Profile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_('phone number must not consist of space and requires country code.eg : +79546748973'))

    phone = models.CharField(validators=[phone_regex], max_length=50, verbose_name=_('phone'))
    region = models.CharField(max_length=255, verbose_name=_('region of residence'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, unique=True)

    image = models.OneToOneField(
        File,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('profile photo')
    )

    def __str__(self):
        return f'{self.user}'

    @property
    def age(self):
        if self.user.birthday:
            today = now()
            return today.year - self.user.birthday.year - (
                    (today.month, today.day) < (self.user.birthday.month, self.user.birthday.day))
        return 0

    @property
    def balance_user(self):
        return self.user.wallet.balance


class Transaction(models.Model):
    user = models.ForeignKey(User, related_name='balance_changes', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_('amount'), default=0, validators=[MinValueValidator(0)])
    descriptions = models.CharField(max_length=255, verbose_name=_('transaction description'))
    datetime = models.DateTimeField(_('date'), default=timezone.now)

    def __str__(self):
        return f'{self.amount}'


class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user`s wallet')
    )
    balance = models.PositiveIntegerField(verbose_name=_('user balance'), default=0)

    @transaction.atomic
    def increase_balance(self, value):
        Transaction.objects.create(
            user=self.user,
            descriptions=f"пополнение счёта на самму {value} от пользователя {self.user.email}",
            amount=value
        )
        self.balance += value

    @transaction.atomic
    def diminish_balance(self, value):
        Transaction.objects.create(
            user=self,
            descriptions=f"списание счёта на самму {value} от пользователя {self.email}",
            amount=value
        )
        self.balance -= value

    def __str__(self):
        return f'{self.balance}'

    class Meta:
        unique_together = (("user", "id"),)
        permissions = (("can_add_money", "top up balance"),)
