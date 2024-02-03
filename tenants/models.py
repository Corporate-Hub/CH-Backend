from django.db import models

from django.utils.translation import gettext_lazy as _
from users.models import BaseModel, UserAccount, ULIDField


class BrandingFile(BaseModel):
    internal_id = ULIDField(_('branding_file_id'), editable=False)
    data = models.BinaryField()
    filename = models.CharField(max_length=500)
    file_size = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f'ID: {self.id}'


class Domain(BaseModel):
    DOMAIN_TYPES = [
        ('prefix', 'Prefix'),
        ('full', 'Full')
    ]
    internal_id = ULIDField(_('domain_id'), editable=False)
    tenant_id = models.CharField(max_length=500)
    domain_name = models.CharField(max_length=500)
    domain_type = models.CharField(max_length=8, choices=DOMAIN_TYPES, default='full', db_index=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    is_default = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f'ID: {self.id}'


class DomainVerification(BaseModel):
    RECORD_TYPES = [
        ('txt', 'TXT'),
        ('cname', 'CNAME')
    ]

    internal_id = ULIDField(_('domain_verification_id'), editable=False)
    tenant_id = models.CharField(max_length=500)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    record = models.TextField(null=True, db_index=True)
    record_type = models.CharField(max_length=6, choices=RECORD_TYPES, default='txt', db_index=True)
    is_verified = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f'ID: {self.id}'


class Tenant(BaseModel):
    internal_id = ULIDField(_('tenant_id'), editable=False)
    name = models.CharField(_('tenant_name'), max_length=100)
    slug = models.SlugField(_('tenant_slug'), max_length=100, unique=True)
    owner_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f'Tenant: {self.owner_id}'
    
    @classmethod
    def get_tenant(cls, **criteria):
        return cls.objects.filter(**criteria)
    
class TenantConfig(BaseModel):
    internal_id = ULIDField(_('tenant_id'), editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, related_name='tenant_config')

    def __str__(self):
        return f'Tenant Config: {self.id}'



class TenantTheme(BaseModel):
    internal_id = ULIDField(_('tenant_theme_id'), editable=False)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, related_name='tenant_theme')
    logo_main = models.ForeignKey(BrandingFile, on_delete=models.SET_NULL, null=True, related_name='theme_logos_main')
    login_page_image = models.ForeignKey(BrandingFile, on_delete=models.SET_NULL, null=True, related_name='theme_login_page_images')
    primary_color = models.CharField(max_length=7, null=True)
    secondary_color = models.CharField(max_length=7, null=True)
    tertiary_color = models.CharField(max_length=7, null=True)
    login_page_text = models.TextField(null=True, db_index=True)
    brand_tagline = models.TextField(null=True, db_index=True)

    def __str__(self):
        return f'ID: {self.id}'


# class TenantConfig(BaseModel):
#     internal_id = ULIDField(_('tenant_config_id'), editable=False)
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)

