# mainapp/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import requests
import hmac
import hashlib
from decimal import Decimal
from .models import Offering 
from .models import ContactMessage

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




# NEW VIEW TO HANDLE FORM SUBMISSION (AJAX)
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