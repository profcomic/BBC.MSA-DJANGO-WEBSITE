from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('leadership/', views.leadership, name='leadership'),
    path('ministries/', views.ministries, name='ministries'),
    path('sermons/', views.sermons, name='sermons'),
    path('inspirations/', views.inspirations, name='inspirations'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('berean-store/', views.berean_store, name='berean_store'),
    path('give/', views.give, name='give'),
    path('process_donation/', views.process_donation, name='process_donation'),
    path('payment/initialize/', views.initialize_payment, name='initialize_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/webhook/', views.paystack_webhook, name='paystack_webhook'),
    path('thank_you/', views.thank_you_view, name='thank_you_page'),
    path('contact/', views.contact_page, name='contact'),
    path('contact/submit/', views.submit_contact, name='submit_contact'), 
    path('gallery/', views.gallery, name='gallery'),
    path('leaders_details/first_family/bshp_A.O/', views.bshp_A_O, name='bshp_A.O'),
     path('leaders_details/reverends/rev_lorine/', views.rev_lorine, name='rev_lorine'),
    path('leaders_details/reverends/rev_odanga/', views.rev_odanga, name='rev_odanga'),
    path('leaders_details/reverends/rev_moses/', views.rev_moses, name='rev_moses'),
    path('leaders_details/pastors/pst_kinzi/', views.pst_kinzi, name='pst_kinzi'),
    path('leaders_details/pastors/pst_kazosi/', views.pst_kazosi, name='pst_kazosi'),
    path('leaders_details/pastors/pst_alfred/', views.pst_alfred, name='pst_alfred'), 
    path('leaders_details/other_leaders/', views.other_leaders, name='other_leaders'), 
    path('ministries_details/kids-ministry/', views.kids_ministry, name='kids_ministry'),
    path('ministries_details/leadership-institute/', views.leadership_institute, name='leadership_institute'),
    path('ministries_details/trendsetters/', views.trendsetters, name='trendsetters'),
    path('ministries_details/marriage_konekt/', views.marriage_konekt, name='marriage_konekt'),
    path('ministries_details/thepriests/', views.thepriests, name='thepriests'),
    path('ministries_details/wisebuilders/', views.wisebuilders, name='wisebuilders'),
    path('ministries_details/firecarriers/', views.firecarriers, name='firecarriers'),



]