# Create your models here.

from django.db import models
from django.utils import timezone

#sermon models
class Sermon(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title
    
#events models
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

#contact us model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=50, default='general')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        # Order newest messages first
        ordering = ['-sent_at'] 
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} - Subject: {self.subject}"
    
#give model
class Offering(models.Model):
    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Donation Details
    giving_type = models.CharField(max_length=50, 
                                   choices=[
                                       ('tithe', 'Tithe & Offerings'),
                                       ('missions', 'Missions & Outreach'),
                                       ('building', 'Building Fund'),
                                       ('men', 'Men Ministry'),
                                       ('women', 'Women Ministry'),
                                       ('youth', 'Youth Ministry'),
                                       ('kids', 'Kids Ministry'),
                                       ('ministries', 'Other Ministries'),
                                       ('department', 'Departmental Fund'),
                                       ('general', 'General Fund'),
                                   ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=50, 
                                 choices=[
                                     ('one-time', 'One-time Gift'),
                                     ('weekly', 'Weekly'),
                                     ('monthly', 'Monthly'),
                                     ('quarterly', 'Quarterly'),
                                     ('annually', 'Annually'),
                                 ])
    notes = models.TextField(blank=True)

    # Transaction/Record Keeping
    date_given = models.DateTimeField(default=timezone.now)
    # NOTE: You SHOULD NOT save sensitive payment info (card number, CVV)
    # The actual transaction would be handled by a third-party payment processor (Stripe, PayPal, M-Pesa API, etc.)
    # You only save a transaction ID.
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    # Paystack Integration Fields
    payment_status = models.CharField(max_length=20, 
                                     choices=[
                                         ('pending', 'Pending'),
                                         ('success', 'Success'),
                                         ('failed', 'Failed'),
                                         ('abandoned', 'Abandoned'),
                                     ],
                                     default='pending')
    paystack_reference = models.CharField(max_length=255, unique=True, blank=True, null=True)
    payment_channel = models.CharField(max_length=50, blank=True, null=True)  # card, bank, ussd, etc.
    paid_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"${self.amount} - {self.get_giving_type_display()} by {self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-date_given']


# Newsletter Subscription Model
class NewsletterSubscriber(models.Model):
    SUBSCRIPTION_STATUS = [
        ('active', 'Active'),
        ('unsubscribed', 'Unsubscribed'),
        ('bounced', 'Bounced'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Subscription preferences
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='active')
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    
    # Interests (what they want to receive)
    interested_in_events = models.BooleanField(default=True)
    interested_in_sermons = models.BooleanField(default=True)
    interested_in_ministries = models.BooleanField(default=True)
    interested_in_news = models.BooleanField(default=True)
    
    # Tracking
    confirmation_sent = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) - {self.status}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


# ============================================
# BEREAN STORE MODELS
# ============================================

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductCategory(models.Model):
    """Categories for store products"""
    CATEGORY_CHOICES = [
        ('books', 'Books & Literature'),
        ('merchandise', 'Merchandise'),
        ('magazines', 'Magazines'),
        ('services', 'Media Services'),
        ('food', 'Food & Snacks'),
        ('beverages', 'Beverages'),
        ('cakes', 'Cakes & Pastries'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-box')  # FontAwesome icon class
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'display_name']
        verbose_name_plural = "Product Categories"
    
    def __str__(self):
        return self.display_name


class Product(models.Model):
    """Store products"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # For discounts
    
    # Inventory
    stock_quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    requires_preorder = models.BooleanField(default=False)
    preorder_days = models.IntegerField(default=0, help_text="Days needed for pre-order")
    
    # Display
    image = models.ImageField(upload_to='store/products/', blank=True, null=True)
    icon_class = models.CharField(max_length=50, default='fas fa-box')  # FontAwesome icon
    gradient_class = models.CharField(max_length=100, default='from-sky-100 to-blue-200')
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    badge_text = models.CharField(max_length=50, blank=True)  # e.g., "POPULAR", "NEW", "SALE"
    badge_color = models.CharField(max_length=50, blank=True)  # e.g., "bg-green-100 text-green-700"
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_on_sale(self):
        return self.original_price and self.original_price > self.price
    
    @property
    def discount_percentage(self):
        if self.is_on_sale:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0
    
    @property
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0
    
    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()


class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class ProductFeature(models.Model):
    """Product features/specifications"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name} - {self.feature_text}"


class ProductReview(models.Model):
    """Customer reviews"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.product.name} ({self.rating}★)"


class Cart(models.Model):
    """Shopping cart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        return f"Cart - Session {self.session_key}"
    
    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD = [
        ('mpesa', 'Lipa na M-Pesa'),
        ('installments', 'Lipa Mdogo Mdogo'),
        ('pay-before', 'Pay Before Delivery'),
        ('pay-after', 'Pay After Delivery'),
        ('order-now', 'Order Now'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Order Info
    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='store_orders')
    
    # Customer Info
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Delivery Info
    delivery_address = models.TextField(blank=True)
    delivery_notes = models.TextField(blank=True)
    
    # Order Details
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    # Payment Integration
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    mpesa_reference = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # Store name in case product is deleted
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class Wishlist(models.Model):
    """User wishlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Deal(models.Model):
    """Special deals and promotions"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='deals', blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date


class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question