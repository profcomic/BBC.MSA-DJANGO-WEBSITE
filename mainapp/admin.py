
from django.contrib import admin
from .models import (
    Sermon, Event, Offering, ContactMessage, NewsletterSubscriber,
    ProductCategory, Product, ProductImage, ProductFeature, ProductReview,
    Cart, CartItem, Order, OrderItem, Wishlist, Deal, FAQ
)

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


# Newsletter Subscriber admin customization
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'status', 'subscribed_at', 'get_interests', 'confirmation_sent')
    list_filter = ('status', 'interested_in_events', 'interested_in_sermons', 'interested_in_ministries', 'interested_in_news', 'subscribed_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('subscribed_at', 'unsubscribed_at', 'confirmation_token', 'ip_address')
    list_per_page = 50
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Subscription Status', {
            'fields': ('status', 'subscribed_at', 'unsubscribed_at')
        }),
        ('Interests & Preferences', {
            'fields': ('interested_in_events', 'interested_in_sermons', 'interested_in_ministries', 'interested_in_news')
        }),
        ('Tracking Information', {
            'fields': ('confirmation_sent', 'confirmation_token', 'ip_address'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Name'
    
    def get_interests(self, obj):
        interests = []
        if obj.interested_in_events:
            interests.append('Events')
        if obj.interested_in_sermons:
            interests.append('Sermons')
        if obj.interested_in_ministries:
            interests.append('Ministries')
        if obj.interested_in_news:
            interests.append('News')
        return ', '.join(interests) if interests else 'None'
    get_interests.short_description = 'Interests'
    
    # Custom actions
    @admin.action(description='Mark as Active')
    def mark_active(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f"{updated} subscribers marked as active.")
    
    @admin.action(description='Mark as Unsubscribed')
    def mark_unsubscribed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='unsubscribed', unsubscribed_at=timezone.now())
        self.message_user(request, f"{updated} subscribers marked as unsubscribed.")
    
    @admin.action(description='Export Active Subscribers')
    def export_active(self, request, queryset):
        active = queryset.filter(status='active')
        self.message_user(request, f"{active.count()} active subscribers found.")
    
    actions = [mark_active, mark_unsubscribed, export_active]


# ============================================
# BEREAN STORE ADMIN
# ============================================

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'display_name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_available', 'is_featured', 'sales_count', 'created_at')
    list_filter = ('category', 'is_available', 'is_featured', 'is_popular', 'is_new', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    list_editable = ('is_available', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductFeatureInline]
    readonly_fields = ('views_count', 'sales_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'is_available', 'requires_preorder', 'preorder_days')
        }),
        ('Display', {
            'fields': ('image', 'icon_class', 'gradient_class')
        }),
        ('Features', {
            'fields': ('is_featured', 'is_popular', 'is_new', 'badge_text', 'badge_color')
        }),
        ('Statistics', {
            'fields': ('views_count', 'sales_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'is_verified_purchase', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'created_at')
    search_fields = ('name', 'email', 'comment', 'product__name')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    
    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} reviews approved.")
    
    actions = [approve_reviews]


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'item_count', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_key')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'unit_price', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_amount', 'payment_method', 'payment_status', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone')
    list_editable = ('status', 'payment_status')
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'confirmed_at', 'delivered_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Delivery Information', {
            'fields': ('delivery_address', 'delivery_notes')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'transaction_id', 'mpesa_reference')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'delivery_fee', 'total_amount', 'amount_paid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.action(description='Mark as Confirmed')
    def mark_confirmed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='confirmed', confirmed_at=timezone.now())
        self.message_user(request, f"{updated} orders marked as confirmed.")
    
    @admin.action(description='Mark as Delivered')
    def mark_delivered(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='delivered', delivered_at=timezone.now())
        self.message_user(request, f"{updated} orders marked as delivered.")
    
    actions = [mark_confirmed, mark_delivered]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('added_at',)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'start_date', 'end_date', 'is_active', 'is_valid')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    filter_horizontal = ('products',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')
    date_hierarchy = 'created_at'