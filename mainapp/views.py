# mainapp/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import requests
import hmac
import hashlib
import secrets
from decimal import Decimal
from .models import Offering 
from .models import ContactMessage
from .models import NewsletterSubscriber

# ==========================================================
# 1. MINISTRY DATA DEFINITION
# (Define a comprehensive list of all ministries here)
# ==========================================================
ALL_MINISTRIES_DATA = [
    # NOTE: Replace "..." with actual image file names and descriptions.
    {"title": "Berean Leadership Institute", "image": "leadership-ministry.jpg", "description": "Raises world-influencing leaders and ministers of the gospel."},
    {"title": "Trendsetters", "image": "trendsetters.png", "description": "The frontliners in making sure the church is vibrant through prayers, fellowship, Bible study, and outreach."},
    {"title": "Marriage Connet", "image": "marriage-connect.jpg", "description": "Marriage is the basic unit of family, here we make sure marriages are in God's Way."},
    {"title": "Men Fellowship", "image": "men-ministry.jpg", "description": "What Happens when Men raise their Holy Hands and take their position as the heads?."},
    {"title": "BBC Women", "image": "women-fellowship.jpg", "description": "Raising a virtuos and hardworking women for without them, family perish..."},
    {"title": "BBC Youths Ministry", "image": "youths-ministry.jpg", "description": "Youths are the agents of revival in the church."},
    {"title": "BBC-Kids", "image": "kids-ministry.png", "description": "Children's ministry focused on fun, faith-based teaching, and spiritual growth."},
    {"title": "Praise & Worship Ministry", "image": "p&w-ministry.jpg", "description": "Leading people in worshipping and praising GOD through music with our gifts."},
    {"title": "Care & Counselling Ministry", "image": "fellowship.jpg", "description": "Ensuring the wellbeing of everyone irregardless."},
    {"title": "Young Professionals Training", "image": "speech.jpg", "description": "Nurturing the God given gifts and maximizing them.."},
    {"title": "Guest Relations Departments", "image": "belonging.jpg", "description": "Provides a conducive environment for the guests and visitors in our services."},
    {"title": "Home Based Services Departments", "image": "home.jpg", "description": "Connecting believers to their grassroots home fellowships."},
    {"title": "Music & Creative Arts", "image": "music-ministry.jpg", "description": "Leading worship through music, drama, and visual arts."},
    {"title": "Technical & Media", "image": "media-ministry.jpg", "description": "Ensuring the gospel is seen and heard clearly through technology and streaming."},
    {"title": "Intercessory & Prayer", "image": "war-room.jpg", "description": "Dedicated to corporate prayer, spiritual warfare, and supporting the church's needs."},
    {"title": "Evangelism & Outreach", "image": "mentorship.jpg", "description": "Reaching the community with the gospel and engaging in local missions."},
    {"title": "Hospitality & Protocol", "image": "analyst.jpg", "description": "Ensuring every visitor feels welcomed and managing order during services."},
    
]

# ==========================================================
# 2. CORE VIEWS
# ==========================================================

def home(request):
    """
    Renders the home page and prepares the ministry data for the flipping cards.
    """
    
    # 2. Split the list into two columns for the home page slider
    data_length = len(ALL_MINISTRIES_DATA)
    mid_point = data_length // 2
    
    # Col 1 gets the first half, Col 2 gets the second half
    col1_ministries = ALL_MINISTRIES_DATA[:mid_point]
    col2_ministries = ALL_MINISTRIES_DATA[mid_point:]
    
    context = {
        'col1_ministries': col1_ministries,
        'col2_ministries': col2_ministries,
    }

    return render(request, 'mainapp/home.html', context)

# ---

def about(request):
    return render(request, 'mainapp/about.html')

def leadership(request):
    return render(request, 'mainapp/leadership.html')

def ministries(request):
    return render(request, 'mainapp/ministries.html')

def sermons(request):
    return render(request, 'mainapp/sermons.html') 

def inspirations(request):
    return render(request, 'mainapp/inspirations.html') 

def events(request):
    return render(request, 'mainapp/events.html')

def contact(request):
    return render(request, 'mainapp/contact.html')

def contact_page(request):
    return render(request, 'mainapp/contact.html', {})

def berean_store(request):
    return render(request, 'mainapp/berean_store.html')

def give(request):
    return render(request, 'mainapp/give.html')

def thank_you_view(request):
    return render(request, 'mainapp/thank_you.html') 

def gallery(request):
    return render(request, 'mainapp/gallery.html')

def prayer_fasting_guide(request):
    return render(request, 'mainapp/resources/prayer_fasting_guide.html')

def weekly_bulletin(request):
    return render(request, 'mainapp/resources/weekly_bulletin.html')

def testimonies(request):
    return render(request, 'mainapp/resources/testimonies.html')

def privacy(request):
    return render(request, 'mainapp/privacy.html')

def terms_of_use(request):
    return render(request, 'mainapp/terms-of-use.html')

def bshp_A_O(request):
    context = {
        'leader_full_name': "BISHOP DR. IBRAHIM ANG'ANA OYOTI", 
        'page_title_nav': "Bishop Ibrahim",   # Short name for the breadcrumb navigation
    }
    return render(request, 'mainapp/leaders_details/first_family/bshp_A.O.html', context)

def rev_lorine(request):
    context = {
        'leader_full_name': "REVEREND LORINE PAMELA ANG'ANA",
        'page_title_nav': "Reverend Lorine",
    }
    return render(request, 'mainapp/leaders_details/first_family/rev_lorine.html', context)

def rev_odanga(request):
    context = {
        'leader_full_name': "REVEREND CONSTANCE ODANGA OJWANG",
        'page_title_nav': "Reverend Odanga",
    }
    return render(request, 'mainapp/leaders_details/reverends/rev_odanga.html', context)

def rev_moses(request):
    context = {
        'leader_full_name': "REVEREND MOSES OYOTI",
        'page_title_nav': "Reverend Moses",
    }
    return render(request, 'mainapp/leaders_details/reverends/rev_moses.html', context)

def pst_kinzi(request):
    context = {
        'leader_full_name': "PASTOR SALVESTIN KINZI MUHANDALE",
        'page_title_nav': "Pastor Kinzi",
    }
    return render(request, 'mainapp/leaders_details/pastors/pst_kinzi.html', context)

def pst_kazosi(request):
    context = {
        'leader_full_name': "PASTOR AGNESS KAZOSI",
        'page_title_nav': "Pastor Kazosi",
    }
    return render(request, 'mainapp/leaders_details/pastors/pst_kazosi.html', context)

def pst_alfred(request):
    context = {
        'leader_full_name': "PASTOR ALFRED MATAI GECHURE", 
        'page_title_nav': "Pastor Alfred",   
    }
    return render(request, 'mainapp/leaders_details/pastors/pst_alfred.html', context)

def other_leaders(request):
    context = {
        'leader_full_name': "OTHER DEPARTMENTAL LEADERS", 
        'page_title_nav': "Other Leaders",   
    }
    return render(request, 'mainapp/leaders_details/other_leaders.html', context)


def leadership_institute(request):
    context = {
        'ministry_full_name': "BBC LEADERSHIP INSTITUTE", 
        'page_title_nav': "Leadership Institute",   
    }
    return render(request, 'mainapp/ministries_details/leadership-institute.html', context)

def trendsetters(request):
    context = {
        'ministry_full_name': "BBC TRENDSETTERS", 
        'page_title_nav': "Trendsetters",   
    }
    return render(request, 'mainapp/ministries_details/trendsetters.html', context)

def marriage_konekt(request):
    context = {
        'ministry_full_name': "BBC MARRIAGE CONNECT", 
        'page_title_nav': "Marej Konekt",   
    }
    return render(request, 'mainapp/ministries_details/marriage_konekt.html', context)

def thepriests(request):
    context = {
        'ministry_full_name': "BBC MEN FELLOWSHIP", 
        'page_title_nav': "The Priestly Men",   
    }
    return render(request, 'mainapp/ministries_details/thepriests.html', context)

def wisebuilders(request):
    context = {
        'ministry_full_name': "BBC WOMEN FELLOWSHIP", 
        'page_title_nav': "The Wise Women",   
    }
    return render(request, 'mainapp/ministries_details/wisebuilders.html', context)

def firecarriers(request):
    context = {
        'ministry_full_name': "BBC YOUTHS MINISTRY", 
        'page_title_nav': "The Fire Blaizers",   
    }
    return render(request, 'mainapp/ministries_details/firecarriers.html', context)

def kids_ministry(request):
    context = {
        'ministry_full_name': "BBC KIDS MINISTRY", 
        'page_title_nav': "Kids Ministry",   
    }
    return render(request, 'mainapp/ministries_details/kids-ministry.html', context)

def music_ministry(request):
    context = {
        'ministry_full_name': "BBC MUSIC MINISTRY", 
        'page_title_nav': "Music Ministry",   
    }
    return render(request, 'mainapp/ministries_details/music-ministry.html', context)

def media_ministry(request):
    context = {
        'ministry_full_name': "BBC MEDIA MINISTRY", 
        'page_title_nav': "Media Ministry",   
    }
    return render(request, 'mainapp/ministries_details/media-ministry.html', context)

def hospitality_ministry(request):
    context = {
        'ministry_full_name': "BBC HOSPITALITY MINISTRY", 
        'page_title_nav': "Hospitality Ministry",   
    }
    return render(request, 'mainapp/ministries_details/hospitality-ministry.html', context)

def outreach_ministry(request):
    context = {
        'ministry_full_name': "BBC OUTREACH MINISTRY", 
        'page_title_nav': "Outreach Ministry",   
    }
    return render(request, 'mainapp/ministries_details/outreach-ministry.html', context)

def care_counseling(request):
    context = {
        'ministry_full_name': "BBC CARE AND COUNSELING MINISTRY", 
        'page_title_nav': "Care & Counseling",   
    }
    return render(request, 'mainapp/ministries_details/care-counseling.html', context)

def young_professionals(request):
    context = {
        'ministry_full_name': "BBC YOUNG PROFESSIONALS TRAINING", 
        'page_title_nav': "Young Professionals",   
    }
    return render(request, 'mainapp/ministries_details/young-professionals.html', context)

def guest_relations(request):
    context = {
        'ministry_full_name': "BBC GUEST RELATIONS DEPARTMENT", 
        'page_title_nav': "Guest Relations",   
    }
    return render(request, 'mainapp/ministries_details/guest-relations.html', context)

def hbc_department(request):
    context = {
        'ministry_full_name': "BBC HBC DEPARTMENT", 
        'page_title_nav': "HBC Department",   
    }
    return render(request, 'mainapp/ministries_details/hbc-department.html', context)

def creative_arts(request):
    context = {
        'ministry_full_name': "BBC MUSIC & CREATIVE ARTS MINISTRY", 
        'page_title_nav': "Creative Arts",   
    }
    return render(request, 'mainapp/ministries_details/creative-arts.html', context)

def intercessory_prayer(request):
    context = {
        'ministry_full_name': "BBC INTERCESSORY & PRAYER MINISTRY", 
        'page_title_nav': "Intercessory & Prayer",   
    }
    return render(request, 'mainapp/ministries_details/intercessory-prayer.html', context)


# VIEW TO HANDLE FORM SUBMISSION (AJAX)
@require_POST
def submit_contact(request):
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            
            # Create and save the message object
            ContactMessage.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                subject=data.get('subject'),
                message=data.get('message'),
            )
            
            # Return success response
            return JsonResponse({'success': True, 'message': 'Message received successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
        
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error saving contact message: {e}")
            return JsonResponse({'success': False, 'message': 'An internal error occurred.'}, status=500)
            
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
# ==========================================================
# 3. PAYSTACK PAYMENT VIEWS
# ==========================================================

@require_POST
def initialize_payment(request):
    """
    Initialize Paystack payment and return payment URL
    """
    try:
        data = json.loads(request.body)
        
        # Extract donation details
        amount = float(data.get('amount', 0))
        email = data.get('email')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        phone = data.get('phone', '')
        giving_type = data.get('givingType', 'tithe')
        frequency = data.get('frequency', 'one-time')
        notes = data.get('notes', '')
        
        # Convert amount to kobo (Paystack uses smallest currency unit)
        amount_in_kobo = int(amount * 100)
        
        # Create offering record with pending status
        offering = Offering.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            giving_type=giving_type,
            amount=Decimal(str(amount)),
            frequency=frequency,
            notes=notes,
            payment_status='pending'
        )
        
        # Initialize Paystack transaction
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "email": email,
            "amount": amount_in_kobo,
            "reference": f"BBC-{offering.id}-{offering.date_given.strftime('%Y%m%d%H%M%S')}",
            "callback_url": request.build_absolute_uri('/payment/callback/'),
            "metadata": {
                "offering_id": offering.id,
                "donor_name": f"{first_name} {last_name}",
                "giving_type": giving_type,
                "frequency": frequency
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        if response_data.get('status'):
            # Update offering with Paystack reference
            offering.paystack_reference = response_data['data']['reference']
            offering.save()
            
            return JsonResponse({
                'success': True,
                'authorization_url': response_data['data']['authorization_url'],
                'reference': response_data['data']['reference']
            })
        else:
            offering.payment_status = 'failed'
            offering.save()
            return JsonResponse({
                'success': False,
                'message': response_data.get('message', 'Payment initialization failed')
            }, status=400)
            
    except Exception as e:
        print(f"Error initializing payment: {e}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while processing your request'
        }, status=500)


def payment_callback(request):
    """
    Handle Paystack payment callback
    """
    reference = request.GET.get('reference')
    
    if not reference:
        return redirect('give')
    
    # Verify transaction
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        
        if response_data.get('status') and response_data['data']['status'] == 'success':
            # Update offering record
            offering = Offering.objects.get(paystack_reference=reference)
            offering.payment_status = 'success'
            offering.transaction_id = response_data['data']['id']
            offering.payment_channel = response_data['data']['channel']
            offering.paid_at = response_data['data']['paid_at']
            offering.save()
            
            return redirect('thank_you_page')
        else:
            return redirect('give')
            
    except Offering.DoesNotExist:
        return redirect('give')
    except Exception as e:
        print(f"Error verifying payment: {e}")
        return redirect('give')


@csrf_exempt
@require_POST
def paystack_webhook(request):
    """
    Handle Paystack webhook notifications
    """
    # Verify webhook signature
    paystack_signature = request.headers.get('X-Paystack-Signature')
    
    if not paystack_signature:
        return JsonResponse({'status': 'error', 'message': 'No signature'}, status=400)
    
    # Compute signature
    hash_object = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
        request.body,
        hashlib.sha512
    )
    expected_signature = hash_object.hexdigest()
    
    if paystack_signature != expected_signature:
        return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)
    
    try:
        payload = json.loads(request.body)
        event = payload.get('event')
        data = payload.get('data')
        
        if event == 'charge.success':
            reference = data.get('reference')
            offering = Offering.objects.get(paystack_reference=reference)
            offering.payment_status = 'success'
            offering.transaction_id = data.get('id')
            offering.payment_channel = data.get('channel')
            offering.paid_at = data.get('paid_at')
            offering.save()
            
        elif event == 'charge.failed':
            reference = data.get('reference')
            offering = Offering.objects.get(paystack_reference=reference)
            offering.payment_status = 'failed'
            offering.save()
            
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# Legacy donation processing (kept for backward compatibility)
@require_POST
def process_donation(request):
    """
    Legacy donation processing - redirects to Paystack flow
    """
    return redirect('give')


# ==========================================================
# 4. NEWSLETTER SUBSCRIPTION VIEWS
# ==========================================================

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_POST
def newsletter_subscribe(request):
    """
    Handle newsletter subscription with email confirmation
    """
    try:
        data = json.loads(request.body)
        
        # Extract data
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip() if data.get('phone') else None
        
        # Validate required fields
        if not first_name or not email:
            return JsonResponse({
                'success': False,
                'message': 'First name and email are required.'
            }, status=400)
        
        # Check if email already exists
        existing_subscriber = NewsletterSubscriber.objects.filter(email=email).first()
        
        if existing_subscriber:
            if existing_subscriber.status == 'active':
                return JsonResponse({
                    'success': False,
                    'message': 'This email is already subscribed to our newsletter.'
                }, status=400)
            else:
                # Reactivate subscription
                existing_subscriber.status = 'active'
                existing_subscriber.first_name = first_name
                existing_subscriber.last_name = last_name
                existing_subscriber.phone = phone
                existing_subscriber.interested_in_events = data.get('interested_in_events', True)
                existing_subscriber.interested_in_sermons = data.get('interested_in_sermons', True)
                existing_subscriber.interested_in_ministries = data.get('interested_in_ministries', True)
                existing_subscriber.interested_in_news = data.get('interested_in_news', True)
                existing_subscriber.save()
                
                subscriber = existing_subscriber
                is_new = False
        else:
            # Create new subscriber
            subscriber = NewsletterSubscriber.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                interested_in_events=data.get('interested_in_events', True),
                interested_in_sermons=data.get('interested_in_sermons', True),
                interested_in_ministries=data.get('interested_in_ministries', True),
                interested_in_news=data.get('interested_in_news', True),
                ip_address=get_client_ip(request),
                confirmation_token=secrets.token_urlsafe(32)
            )
            is_new = True
        
        # Send welcome email
        try:
            send_welcome_email(subscriber, request)
            subscriber.confirmation_sent = True
            subscriber.save()
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            # Don't fail the subscription if email fails
        
        return JsonResponse({
            'success': True,
            'message': f'Thank you for subscribing! A welcome email has been sent to {email}.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid data format.'
        }, status=400)
    except Exception as e:
        print(f"Newsletter subscription error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again later.'
        }, status=500)


def send_welcome_email(subscriber, request):
    """
    Send welcome email to new newsletter subscriber
    """
    subject = 'Welcome to BBC Newsletter - Berean Baptist Church Mombasa'
    
    # Create unsubscribe link
    unsubscribe_url = request.build_absolute_uri(
        f'/newsletter/unsubscribe/{subscriber.confirmation_token}/'
    )
    
    # Prepare context for email template
    context = {
        'subscriber': subscriber,
        'unsubscribe_url': unsubscribe_url,
        'current_year': 2025,
    }
    
    # Render HTML email
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; padding: 12px 30px; background: #3B82F6; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
            .interests {{ background: white; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .interest-item {{ display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 5px 10px; border-radius: 3px; margin: 5px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to BBC Newsletter!</h1>
                <p>Berean Baptist Church - Mombasa</p>
            </div>
            <div class="content">
                <h2>Hello {subscriber.first_name}!</h2>
                <p>Thank you for subscribing to our newsletter. We're thrilled to have you as part of our community!</p>
                
                <p>You'll now receive:</p>
                <div class="interests">
                    {"<span class='interest-item'>📅 Event Updates</span>" if subscriber.interested_in_events else ""}
                    {"<span class='interest-item'>🎤 Sermon Highlights</span>" if subscriber.interested_in_sermons else ""}
                    {"<span class='interest-item'>⛪ Ministry News</span>" if subscriber.interested_in_ministries else ""}
                    {"<span class='interest-item'>📰 Church News</span>" if subscriber.interested_in_news else ""}
                </div>
                
                <p><strong>What to expect:</strong></p>
                <ul>
                    <li>Weekly inspirational messages</li>
                    <li>Upcoming events and programs</li>
                    <li>Sermon highlights and resources</li>
                    <li>Ministry updates and opportunities</li>
                    <li>Exclusive content for our community</li>
                </ul>
                
                <p>Stay connected with us:</p>
                <p>
                    📧 Email: info@bereanbaptistmombasa.org<br>
                    📱 Phone: +254 XXX XXX XXX<br>
                    📍 Location: Mombasa, Kenya
                </p>
                
                <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 14px; color: #6b7280;">
                    If you didn't subscribe to this newsletter, you can safely ignore this email or 
                    <a href="{unsubscribe_url}" style="color: #3B82F6;">unsubscribe here</a>.
                </p>
            </div>
            <div class="footer">
                <p>&copy; {context['current_year']} Berean Baptist Church - Mombasa. All rights reserved.</p>
                <p>
                    <a href="{unsubscribe_url}" style="color: #6b7280;">Unsubscribe</a> | 
                    <a href="{request.build_absolute_uri('/privacy/')}" style="color: #6b7280;">Privacy Policy</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_message = f"""
    Welcome to BBC Newsletter!
    
    Hello {subscriber.first_name}!
    
    Thank you for subscribing to our newsletter. We're thrilled to have you as part of our community!
    
    You'll receive weekly updates about events, sermons, ministries, and church news.
    
    Stay connected with us:
    Email: info@bereanbaptistmombasa.org
    Phone: +254 XXX XXX XXX
    Location: Mombasa, Kenya
    
    If you didn't subscribe, you can unsubscribe here: {unsubscribe_url}
    
    © {context['current_year']} Berean Baptist Church - Mombasa
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bereanbaptistmombasa.org',
        to=[subscriber.email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send()


def newsletter_unsubscribe(request, token):
    """
    Handle newsletter unsubscription
    """
    try:
        subscriber = NewsletterSubscriber.objects.get(confirmation_token=token)
        subscriber.status = 'unsubscribed'
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()
        
        return render(request, 'mainapp/newsletter_unsubscribed.html', {
            'subscriber': subscriber
        })
    except NewsletterSubscriber.DoesNotExist:
        return render(request, 'mainapp/newsletter_unsubscribed.html', {
            'error': 'Invalid unsubscribe link.'
        })