
from django.contrib import admin
from .models import Sermon, Event, Offering , ContactMessage

admin.site.register(Sermon)
admin.site.register(Event)
# admin.site.register(ContactMessage)

#contact message admin customization
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at', 'is_read')
    # Fields to use as filters
    list_filter = ('subject', 'is_read', 'sent_at')
    # Fields to search
    search_fields = ('name', 'email', 'message')
    # Make 'is_read' editable directly in the list view
    list_editable = ('is_read',)

    # Custom action to mark selected messages as read
    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} messages marked as read.")

    actions = [mark_as_read]

# Offering admin customization with Paystack fields
@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ('get_donor_name', 'email', 'amount', 'giving_type', 'payment_status', 'payment_channel', 'date_given')
    list_filter = ('payment_status', 'giving_type', 'frequency', 'payment_channel', 'date_given')
    search_fields = ('first_name', 'last_name', 'email', 'paystack_reference', 'transaction_id')
    readonly_fields = ('date_given', 'paystack_reference', 'transaction_id', 'paid_at')
    list_per_page = 50
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Donation Details', {
            'fields': ('giving_type', 'amount', 'frequency', 'notes')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_channel', 'paystack_reference', 'transaction_id', 'date_given', 'paid_at')
        }),
    )
    
    def get_donor_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_donor_name.short_description = 'Donor Name'
    
    # Custom action to export successful donations
    @admin.action(description='Export successful donations')
    def export_successful(self, request, queryset):
        successful = queryset.filter(payment_status='success')
        self.message_user(request, f"{successful.count()} successful donations found.")
    
    actions = [export_successful]