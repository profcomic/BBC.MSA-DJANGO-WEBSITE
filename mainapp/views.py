from django.shortcuts import render

def home(request):
    return render(request, 'mainapp/home.html')

def about(request):
    return render(request, 'mainapp/about.html')

def leadership(request):
    return render(request, 'mainapp/leadership.html')

def ministries(request):
    return render(request, 'mainapp/ministries.html')

def sermons(request):
    return render(request, 'mainapp/sermons.html') 

def blog(request):
    return render(request, 'mainapp/blog.html')

def events(request):
    return render(request, 'mainapp/events.html')

def contact(request):
    return render(request, 'mainapp/contact.html')

def berean_times_magazine(request):
    return render(request, 'mainapp/berean_times_magazine.html')

def give(request):
    return render(request, 'mainapp/give.html')