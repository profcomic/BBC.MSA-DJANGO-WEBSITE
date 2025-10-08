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


    def __str__(self):
        return f"${self.amount} - {self.get_giving_type_display()} by {self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-date_given']