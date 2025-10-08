# mainapp/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
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
    return render(request, 'mainapp/leaders_details/first_family/pst_alfred.html', context)

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

def kids_ministry(request):
    context = {
        'ministry_full_name': "BBC KIDS MINISTRY", 
        'page_title_nav': "Kids Ministry",   
    }
    return render(request, 'mainapp/ministries_details/kids-ministry.html', context)

def leadership_institute(request):
    context = {
        'ministry_full_name': "BBC LEADERSHIP INSTITUTE", 
        'page_title_nav': "Leadership Institute",   
    }
    return render(request, 'mainapp/ministries_details/leadership-institute.html', context)



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
# 3. TRANSACTION VIEWS
# ==========================================================

@require_POST
def process_donation(request):
    """
    Handles form submission for donations and saves the record to the database.
    NOTE: Integration with a real payment gateway (like M-Pesa or PayPal) 
    is required here before redirection.
    """
    try:
        # Get data from the POST request, handling potential empty/missing fields
        amount_value = request.POST.get('customAmountInput') or request.POST.get('selectedAmount')
        
        # Save the offering record
        new_offering = Offering.objects.create(
            first_name=request.POST.get('firstName', ''),
            last_name=request.POST.get('lastName', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            giving_type=request.POST.get('givingType', 'Tithes'), # Default to Tithes if missing
            amount=amount_value, 
            frequency=request.POST.get('frequency', 'One-Time'),
            notes=request.POST.get('notes', ''),
            # transaction_id='PLACE_PAYMENT_GATEWAY_ID_HERE' 
        )
        
        # Redirect to the thank you page after successful creation (and payment processing)
        return redirect('thank_you_view') 
    
    except Exception as e:
        # Handle errors (e.g., failed validation, database error)
        print(f"Error saving donation: {e}")
        # Re-render the give page with an error message
        return render(request, 'mainapp/give.html', {'error': 'There was an error processing your donation. Please check your details.'})