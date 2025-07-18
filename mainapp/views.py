from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def sermons(request):
<<<<<<< HEAD
    return render(request, 'mainapp/sermons.html')

def give(request):
    return render(request, 'mainapp/give.html')

def events(request):
    return render(request, 'mainapp/events.html')

def contact(request):
    return render(request, 'mainapp/contact.html')
=======
    return render(request, 'sermons.html')

def events(request):
    return render(request, 'events.html')

def contacts(request):
    return render(request, 'contacts.html')
>>>>>>> 0bf4b630fa1318caf786ac0e69a9ea06922ce338
