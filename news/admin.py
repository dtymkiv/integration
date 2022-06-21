from django.contrib import admin
from news. models import Action, Article


# Register your models here.
admin.site.register([Action, Article])