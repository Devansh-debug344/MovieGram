from django.contrib import admin
from .models import Note , Movie , Category
# Register your models here.
admin.site.register(Note)
admin.site.register(Movie)
admin.site.register(Category)