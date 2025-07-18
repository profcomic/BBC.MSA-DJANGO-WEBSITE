from django.shortcuts import render

def home(request):
    return render(request, 'mainapp/home.html')

def about(request):
    return render(request, 'mainapp/about.html')

def sermons(request):
    return render(request, 'mainapp/sermons.html')

def events(request):
    return render(request, 'mainapp/events.html')

def contact(request):
    return render(request, 'mainapp/contact.html')

def give(request):
    return render(request, 'mainapp/give.html')