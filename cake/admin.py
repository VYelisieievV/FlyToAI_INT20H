from django.contrib import admin
from .models import Forecast, Visual, Chart

admin.site.register(Forecast)
admin.site.register(Visual)
admin.site.register(Chart)

class VisualDisplayAdmin(admin.ModelAdmin):
    list_display = ('user', 'path', 'picture')
    readonly_fields = ('picture')
    fields = ('user', 'path', 'picture')
# Register your models here.
class ChartDisplayAdmin(admin.ModelAdmin):
    list_display = ('date', 'type')
    readonly_fields = ('date', 'type')
    fields = ('date', 'type')
