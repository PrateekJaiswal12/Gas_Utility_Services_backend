from django.contrib import admin

# Register your models here.

from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'type_of_request', 'status', 'date_submitted', 'date_resolved')
    list_filter = ('status', 'type_of_request', 'date_submitted')
    search_fields = ('customer__username', 'customer__email', 'details')
    readonly_fields = ('date_submitted', 'date_resolved')
    ordering = ('-date_submitted',)
