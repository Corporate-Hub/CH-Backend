from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .utils import UserAccountManager

from django.db.models.fields import UUIDField
from ulid import new as ulid_new

class ULIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 26  # ULID has a fixed length of 26 characters
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = str(ulid_new())
            setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)

class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.CharField(max_length=500, blank=True)
    updated_by = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.date_modified = timezone.now()
        super().save(*args, **kwargs)


class Country(BaseModel):

    internal_id = ULIDField(_('country_ulid'), editable = False)
    name = models.CharField(_('country name'), max_length=255)
    isd_code = models.CharField(_('isd code'), max_length=50)
    alpha2 = models.CharField(_('alpha 2'), max_length=100)
    alpha3 = models.CharField(_('apha 3'), max_length=100)
    currency = models.CharField(_('currency'), max_length=100)
    currency_symbol = models.CharField(_('currency symbol'), max_length=100)
    currency_code = models.CharField(_('currency code'), max_length=100)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    @classmethod
    def get_country(cls, **criteria):
        return cls.objects.filter(**criteria)

    def __str__(self):
        return self.name


class State(BaseModel):

    internal_id = ULIDField(_('state_uuid'), editable = False)
    name = models.CharField(_('state'), max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    @classmethod
    def get_state(cls, **criteria):
        return cls.objects.filter(**criteria)


# class City(BaseModel):
#     internal_id = ULIDField(_('city_uuid'), editable=False)
#     name = models.CharField(_('city_name'), max_length=255)
#     state = models.ForeignKey(State, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'City'
#         verbose_name_plural = 'Cities'

#     @classmethod
#     def get_city(cls, **criteria):
#         return cls.objects.filter(**criteria)

#     def __str__(self):
#         return self.name

class PhoneNumber(BaseModel):

    internal_id = ULIDField(_('phone_ulid'), editable = False)
    isd_code = models.CharField(models.CharField(_('isd_code'), blank=True, help_text="isd_code"))
    phone = models.CharField(models.CharField(_('phone_number'), blank=True, help_text="phone number"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'

    @classmethod
    def get_phone_number(cls, **criteria):
        return cls.objects.filter(**criteria)


class Address(BaseModel):

    internal_id = ULIDField(_('address_id'), editable=False)
    address_1 = models.CharField(_('address_1'), max_length=100)
    address_2 = models.CharField(_('address_2'), max_length=100)
    zip_code = models.CharField(_('zip_code'), max_length=50)
    city = models.CharField(_('city'), max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    @classmethod
    def get_address(cls, **criteria):
        return cls.objects.filter(**criteria)


class Company(BaseModel):

    internal_id = ULIDField(_('role_id'), editable=False)
    name = models.CharField(_('company_name'), max_length=100)
    branch = models.CharField(_('company_branch'), max_length=100)
    company_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Company'

    def __str__(self):
        return self.name

    @classmethod
    def get_company(cls, **criteria):
        return cls.objects.filter(**criteria)


class Role(BaseModel):

    internal_id = ULIDField(_('role_id'), editable=False)
    slug =  models.SlugField(_('slug'), max_length=100, unique=True, db_index=True)
    name = models.CharField(_('role_name'), max_length=100)
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name
    
    @classmethod
    def get_role(cls, **criteria):
        return cls.objects.filter(**criteria)


class UserAccount(AbstractBaseUser, PermissionsMixin, BaseModel):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    internal_id = ULIDField(_('user_id'), editable = False)
    email = models.EmailField(_('email'), max_length=255, unique=True)
    secondary_email = models.EmailField(_('secondary email'),max_length=254, help_text="secondary email address")
    first_name = models.CharField(_('first name'),max_length=254, help_text="First Name of the User")
    last_name = models.CharField(_('last name'),max_length=254, help_text="Last Name of the User")
    gender = models.CharField(_('sex'),max_length=6, choices=GENDER_CHOICES)
    dob = models.DateTimeField(_('date of birth'), auto_now_add=True)
    employee_code = models.CharField(_('employee_code'), max_length=50)
    joining_date = models.DateTimeField(_('joining date'), auto_now=True)
    address = models.ForeignKey(Address ,on_delete=models.CASCADE, null=True)
    phone = models.ForeignKey(PhoneNumber ,on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(_("is_staff"), default=False)
    attendance = models.ForeignKey('workflow.Attendance', on_delete=models.CASCADE, null=True)
    leave_request = models.ForeignKey('workflow.LeaveRequest', on_delete=models.CASCADE, null=True)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_user(cls, **criteria):
        return cls.objects.filter(**criteria)


class Invitation(BaseModel):

    internal_id = ULIDField(_('invitation_id'), editable = False)
    inviter_id = models.ForeignKey(UserAccount,  on_delete=models.CASCADE, related_name='invitations')
    first_name = models.CharField(_('first name'), max_length=254)
    last_name = models.CharField(_('last name'), max_length=254)
    email = models.EmailField(_('email'), max_length=255, unique=True)
    role = models.ForeignKey(Role,  on_delete=models.CASCADE, related_name='invitations')
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='invitations')

    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'

    @classmethod
    def get_invitation(cls, **criteria):
        return cls.objects.filter(**criteria)


class InvitationHistory(BaseModel):

    internal_id = ULIDField(_('invitation_id'), editable = False)
    email = models.EmailField(_('email'), max_length=255, unique=False)
    token = models.TextField()
    expiry_date = models.DateTimeField(_('expires_at'))

    class Meta:
        verbose_name = 'Invitation History'
        verbose_name_plural = 'Invitation History'

    @classmethod
    def get_invitation_history(cls, **criteria):
        return cls.objects.filter(**criteria)







