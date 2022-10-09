from django.db import models
from django.conf import settings
from django.forms import CharField
# Create your models here.
# from django.utils.translation import gettext_lazy as _
# from .constants import PaymentStatus
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

from django.contrib.auth.models import PermissionsMixin

from django.db.models import Q
from datetime import timedelta, timezone
import datetime


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    # email = LowercaseEmailField(_('email address'), unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Cost(models.Model):
    cost = models.IntegerField()


class Water(models.Model):
    quantity = models.IntegerField()
    date = models.CharField(max_length=20)
    User = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Due(models.Model):
    Due = models.IntegerField()
    User = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# class Order(models.Model):

#     Duement_status_choices = (
#         (1, 'SUCCESS'),
#         (2, 'FAILURE' ),
#         (3, 'PENDING'),
#     )
#     User = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


#     total_amount = models.FloatField()
#     payment_status = models.IntegerField(choices = payment_status_choices, default=3)
#     order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
#     datetime_of_payment = models.DateTimeField(default=timezone.now)
#     # related to razorpay
#     razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
#     razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
#     razorpay_signature = models.CharField(max_length=500, null=True, blank=True)


#     def save(self, *args, **kwargs):
#         if self.order_id is None and self.datetime_of_payment and self.id:
#             self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
#         return super().save(*args, **kwargs)

#     def __str__(self):
#         return self.user.email + " " + str(self.id)
