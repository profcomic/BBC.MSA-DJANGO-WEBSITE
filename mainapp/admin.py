
# Register your models here.
from django.contrib import admin
from .models import Sermon, Event, Offering , ContactMessage

admin.site.register(Sermon)
admin.site.register(Event)
admin.site.register(Offering)
# admin.site.register(ContactMessage)

#contact message admin customization
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Fields to display in the list view
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