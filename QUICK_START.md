# Quick Start Guide - Paystack Integration

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Your Paystack Keys
1. Go to https://dashboard.paystack.com
2. Sign up or log in
3. Navigate to **Settings** → **API Keys & Webhooks**
4. Copy your **Test Secret Key** and **Test Public Key**

### Step 3: Update Settings
Edit `BBCMAINWEBSITE/settings.py`:

```python
# Replace these with your actual keys
PAYSTACK_SECRET_KEY = 'sk_test_your_secret_key_here'
PAYSTACK_PUBLIC_KEY = 'pk_test_your_public_key_here'
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Start the Server
```bash
python manage.py runserver
```

### Step 6: Test It!
1. Visit http://localhost:8000/give/
2. Fill in the donation form
3. Use test card: **4084084084084081**
4. CVV: **408**, PIN: **0000**, OTP: **123456**

## ✅ That's It!

Your Paystack integration is now ready. Check `PAYSTACK_INTEGRATION.md` for detailed documentation.

## 🔧 Common Issues

**Issue:** Payment initialization fails
- **Fix:** Check your secret key is correct in settings.py

**Issue:** Migration errors
- **Fix:** Delete `db.sqlite3` and run migrations again (development only!)

**Issue:** Module not found errors
- **Fix:** Make sure you're in the virtual environment: `venv\Scripts\activate` (Windows)

## 📚 Next Steps

- Set up webhooks for production
- Configure email receipts
- Switch to live keys when ready to go live
- Review security best practices in the full documentation
