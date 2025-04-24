from django.contrib import admin
from .models import Customer
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_id', 'init_email', 'init_email_confirmed')  # Fields to display in the list view
    search_fields = ('user__username', 'stripe_id', 'init_email')  # Fields to search by
    list_filter = ('init_email_confirmed',)  # Add filters for boolean fields

# Register the model with the custom admin class
admin.site.register(Customer, CustomerAdmin)