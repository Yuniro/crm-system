from django.conf import settings
from django.db import models
import pytz
from django.contrib.auth.models import AbstractUser, Group, Permission
from managers import CustomUserManager


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    domains = models.CharField(max_length=100)
    logo = models.ImageField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    rank = models.CharField(max_length=50)
    permission = models.CharField(max_length=100, choices=settings.PERMISSIONS)

    def __str__(self):
        return self.name


class Employer(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    is_owner = models.BooleanField(blank=True, null=True)
    language = models.CharField(max_length=30, blank=True)
    passport = models.CharField(max_length=25, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    permission = models.TextField(default=None, blank=True, null=True)
    is_confirm = models.BooleanField(blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text=
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ,
        related_name="employer_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="employer_set",
        related_query_name="employer",
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Client (models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    date_joined = models.DateField()
    last_login = models.DateField()
    language = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50)
    avatar = models.ImageField()
    last_name = models.CharField(max_length=50)
    doc_list = models.CharField(max_length=100)
    employer_lead = models.ForeignKey(Employer, on_delete=models.DO_NOTHING, related_name='+')
    employer_lead_type = models.CharField(choices=[
        ['fixed', 'фиксированая ставка'],
        ['percent', 'процент от сделки'],
    ], max_length=100)
    employer_lead_amount = models.FloatField()
    employer = models.ForeignKey(Employer, on_delete=models.DO_NOTHING, related_name='+')
    employer_type = models.CharField(choices=[
        ['fixed', 'фиксированая ставка'],
        ['percent', 'процент от сделки'],
    ], max_length=100)
    employer_amount = models.FloatField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Currency (models.Model):
    name = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    sign = models.CharField(max_length=1)
    fraction_digits = models.IntegerField()
    is_active = models.BooleanField()


class ExchangeRate (models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    rate = models.FloatField()
    date_created = models.DateTimeField()

    def __str__(self):
        return self.currency


class Payment (models.Model):
    is_active = models.BooleanField()
    currency = models.CharField(max_length=3)
    purse = models.IntegerField()
    api_key = models.CharField(max_length=100)
    handler_url = models.URLField()
    handler_method = models.CharField(max_length=100)
    button_title = models.CharField(max_length=12)
    button_url = models.URLField()
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    language = models.CharField(max_length=20)


class Transaction (models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    created_date = models.DateField()
    created_by = models.CharField(max_length=100)
    is_completed = models.BooleanField()
    completed_date = models.DateField()
    amount = models.FloatField()
    currency = models.CharField(max_length=3)
    comment = models.CharField(max_length=300)
    data = models.TextField()


class Expenses (models.Model):
    amount = models.FloatField()
    currency = models.CharField(max_length=3)
    comment = models.CharField(max_length=300)
    date_created = models.DateField()


class Country (models.Model):
    country = models.CharField(max_length=2)
    name = models.CharField(max_length=20)
    code = models.IntegerField()
    currency = models.CharField(max_length=3)
    time_zone = models.CharField(default='UTC', choices=[(tz, tz) for tz in pytz.all_timezones], max_length=1000)


class Tour (models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    client = models.CharField(max_length=30)
    client_list = models.TextField()
    name = models.CharField(max_length=100)
    price = models.FloatField()
    currency = models.CharField(max_length=3)
    exchange_rate = models.FloatField()
    member_count = models.IntegerField()
    status = models.CharField(max_length=10)
    created_date = models.DateField()
    finished_date = models.DateField()


class Notification (models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    email_list = models.TextField()
    phone_list = models.TextField()
    event = models.CharField(max_length=100)
    event_time = models.TimeField()


class Report (models.Model):
    changes = models.TextField()
    time = models.TimeField()


class Container (models.Model):
    information = models.TextField()
