from django.contrib import admin
from restaurant import models

admin.site.register(models.Vote)
admin.site.register(models.Menu)
admin.site.register(models.Restaurant)
