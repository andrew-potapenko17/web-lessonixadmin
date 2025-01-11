from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'adminpanel/home.html', context=context)
