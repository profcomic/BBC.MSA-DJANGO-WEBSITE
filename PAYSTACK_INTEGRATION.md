# Paystack Payment Integration Guide

This document explains how to set up and use Paystack payment integration for the BBC Website donation system.

## Overview

The website now uses Paystack as the payment gateway for processing donations. Paystack is a popular African payment processor that supports multiple payment methods including cards, bank transfers, USSD, and mobile money.

## Features Implemented

- ✅ Secure payment initialization
- ✅ Payment verification and callback handling
- ✅ Webhook support for real-time payment notifications
- ✅ Transaction tracking and status management
- ✅ Support for multiple giving types and frequencies
- ✅ Donor information capture

## Setup Instructions

### 1. Install Dependencies

Run the following command to install required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `Django==5.2.2`
- `pypaystack2==1.1.0` (Paystack Python SDK)
- `requests==2.31.0`
- `python-decouple==3.8`

### 2. Get Paystack API Keys

1. Sign up for a Paystack account at https://paystack.com
2. Log in to your Paystack Dashboard: https://dashboard.paystack.com
3. Navigate to **Settings** → **API Keys & Webhooks**
4. Copy your **Secret Key** and **Public Key**

**Note:** Paystack provides test keys for development and live keys for production.

### 3. Configure Settings

Open `BBCMAINWEBSITE/settings.py` and update the Paystack configuration:

```python
# Paystack Configuration
PAYSTACK_SECRET_KEY = 'sk_test_xxxxxxxxxxxxxxxxxxxxx'  # Replace with your secret key
PAYSTACK_PUBLIC_KEY = 'pk_test_xxxxxxxxxxxxxxxxxxxxx'  # Replace with your public key
```

**Security Best Practice:** For production, use environment variables instead of hardcoding keys:

```python
import os
from decouple import config

PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')
```

Create a `.env` file in your project root:
```
PAYSTACK_SECRET_KEY=sk_live_xxxxxxxxxxxxxxxxxxxxx
PAYSTACK_PUBLIC_KEY=pk_live_xxxxxxxxxxxxxxxxxxxxx
```

### 4. Run Database Migrations

The Offering model has been updated with new Paystack-related fields. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Configure Webhook (Optional but Recommended)

Webhooks allow Paystack to notify your server about payment events in real-time.

1. In your Paystack Dashboard, go to **Settings** → **API Keys & Webhooks**
2. Scroll to the **Webhook URL** section
3. Enter your webhook URL: `https://yourdomain.com/payment/webhook/`
4. Click **Save**

**For local development:** Use a tool like [ngrok](https://ngrok.com/) to expose your local server:
```bash
ngrok http 8000
```
Then use the ngrok URL for your webhook: `https://your-ngrok-url.ngrok.io/payment/webhook/`

## How It Works

### Payment Flow

1. **User fills donation form** on `/give/` page
2. **Form submission** sends data to `/payment/initialize/` endpoint
3. **Backend creates** an Offering record with `pending` status
4. **Paystack transaction** is initialized via API
5. **User is redirected** to Paystack payment page
6. **User completes payment** using their preferred method
7. **Paystack redirects** back to `/payment/callback/` with reference
8. **Backend verifies** the transaction with Paystack API
9. **Offering record** is updated with payment status
10. **User sees** thank you page

### Database Schema

The `Offering` model includes these Paystack-specific fields:

- `payment_status`: Current status (pending, success, failed, abandoned)
- `paystack_reference`: Unique transaction reference from Paystack
- `payment_channel`: Payment method used (card, bank, ussd, etc.)
- `paid_at`: Timestamp when payment was completed
- `transaction_id`: Paystack transaction ID

## API Endpoints

### POST `/payment/initialize/`
Initializes a new payment transaction.

**Request Body:**
```json
{
  "amount": 100.00,
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+254712345678",
  "givingType": "tithe",
  "frequency": "one-time",
  "notes": "Optional notes"
}
```

**Response:**
```json
{
  "success": true,
  "authorization_url": "https://checkout.paystack.com/xxxxx",
  "reference": "BBC-123-20251009193000"
}
```

### GET `/payment/callback/`
Handles redirect after payment completion.

**Query Parameters:**
- `reference`: Transaction reference from Paystack

### POST `/payment/webhook/`
Receives webhook notifications from Paystack (CSRF exempt).

**Headers:**
- `X-Paystack-Signature`: HMAC signature for verification

## Testing

### Test Cards

Paystack provides test cards for development:

**Successful Payment:**
- Card Number: `4084084084084081`
- CVV: `408`
- Expiry: Any future date
- PIN: `0000`
- OTP: `123456`

**Failed Payment:**
- Card Number: `5060666666666666666`
- CVV: Any 3 digits
- Expiry: Any future date

More test cards: https://paystack.com/docs/payments/test-payments/

### Testing Webhooks Locally

1. Install ngrok: `npm install -g ngrok` or download from https://ngrok.com
2. Start your Django server: `python manage.py runserver`
3. In another terminal, run: `ngrok http 8000`
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
5. Set this as your webhook URL in Paystack Dashboard: `https://abc123.ngrok.io/payment/webhook/`

## Currency Support

Paystack supports multiple currencies. The default is **NGN (Nigerian Naira)**.

To change currency, update the initialization payload in `views.py`:

```python
payload = {
    "email": email,
    "amount": amount_in_kobo,
    "currency": "KES",  # Kenyan Shilling
    # ... other fields
}
```

Supported currencies: NGN, GHS, ZAR, KES, USD

**Note:** Amounts are in the smallest currency unit (kobo for NGN, cents for USD/KES).

## Admin Panel

View and manage donations in Django Admin:

1. Access admin at `/admin/`
2. Navigate to **Mainapp** → **Offerings**
3. You can filter by payment status, date, giving type, etc.

To register the model in admin (already done in `admin.py`):

```python
from django.contrib import admin
from .models import Offering

@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'amount', 'giving_type', 'payment_status', 'date_given']
    list_filter = ['payment_status', 'giving_type', 'frequency']
    search_fields = ['first_name', 'last_name', 'email', 'paystack_reference']
```

## Troubleshooting

### Payment initialization fails
- Check that your Paystack secret key is correct
- Verify the amount is greater than 0
- Check Django logs for error messages

### Webhook not receiving events
- Verify webhook URL is correct in Paystack Dashboard
- Check that the URL is publicly accessible (use ngrok for local testing)
- Verify webhook signature validation is working

### Transaction verification fails
- Check that the reference exists in your database
- Verify Paystack secret key is correct
- Check network connectivity to Paystack API

## Security Considerations

1. **Never expose your secret key** in client-side code
2. **Always verify webhook signatures** to prevent spoofing
3. **Use HTTPS** in production for all endpoints
4. **Validate all user inputs** before processing
5. **Store API keys in environment variables**, not in code
6. **Use test keys** for development, live keys only in production

## Going Live

Before going live:

1. ✅ Replace test API keys with live keys
2. ✅ Update webhook URL to production domain
3. ✅ Test with real (small amount) transactions
4. ✅ Verify email receipts are working
5. ✅ Set up proper error logging and monitoring
6. ✅ Review Paystack's go-live checklist: https://paystack.com/docs/payments/go-live/

## Support

- **Paystack Documentation:** https://paystack.com/docs
- **Paystack Support:** support@paystack.com
- **Django Documentation:** https://docs.djangoproject.com

## Additional Features to Consider

- Email receipts after successful payment
- Recurring payment subscriptions
- Payment analytics dashboard
- Export donation reports
- Multi-currency support
- Refund handling

---

**Last Updated:** October 9, 2025
**Integration Version:** 1.0
