from django.apps import apps
from django.contrib import admin

# Get all models from the app
app_models = apps.get_models()

# Register all models in the admin interface
for model in app_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass