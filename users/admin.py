from django.apps import apps
from django.contrib import admin
from users.models import Country, State
# # Get all models from the app
# app_models = apps.get_models()

# # Register all models in the admin interface
# for model in app_models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'isd_code', 'alpha3','alpha2','currency','currency_symbol','currency_code',)
    search_fields = ('name','isd_code','currency','alpha3',)

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country',)

admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)