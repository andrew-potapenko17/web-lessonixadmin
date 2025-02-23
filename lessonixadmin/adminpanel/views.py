from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import cfg
from .decorators import is_authenticated
import pyrebase

firebase = pyrebase.initialize_app(cfg.config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

@is_authenticated
def home(request):
    context = {}
    return render(request, 'adminpanel/home.html', context=context)

def login(request):
    if request.method == 'POST':
        schoolid = request.POST.get('schoolid')
        password = request.POST.get('password')

        print(schoolid, password)

        if (db.child("schools").child(schoolid).get()):
            print(db.child("schools").child(schoolid).child("password").get().val())
            if(db.child("schools").child(schoolid).child("password").get().val() == password):
                print("Succes")

                # store in sessions
                request.session['schoolid'] = str(schoolid)

                return redirect('home')
            else:
                print("Incorrect password")
        else:
            print("No school found")
            

    return render(request, 'login.html')

@is_authenticated
def logout(request):
    request.session.flush()
    return redirect('login')