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
    # get schoolid
    schoolid = request.session.get('schoolid')

    schoolName = db.child("schools").child(schoolid).child("school_name").get().val()
    total_registered = db.child("schools").child(schoolid).child("students_registered").get().val()

    # TODO all values in context

    context = {
        "SCHOOL_NAME": schoolName,
        "SCHOOL_ID": schoolid,
        "TOTAL_REGISTERED": total_registered,
        "WEEK_STATISTIC": [0, 0, 0, 0, 0, 0, 0],
        "LAST_REPORT": "02/24",
        "EVENTS": [],
    }

    return render(request, 'adminpanel/home.html', context=context)

@is_authenticated
def classesPage(request):
    schoolid = request.session.get('schoolid')
    
    classes_data = db.child("school_classes").child(schoolid).get().val()
    
    classes_list = []
    
    if classes_data:
        for class_name, class_value in classes_data.items():
            lead_teacher = class_value.get("leadTeacher", "Невідомо")
            
            students = class_value.get("students", {})
            students_count = len(students)

            print(students)
            
            classes_list.append({
                "name": class_name,
                "leadTeacher": lead_teacher,
                "studentsCount": students_count
            })
    
    context = {
        "classes": classes_list
    }
    
    return render(request, 'adminpanel/classes.html', context)

def login(request):
    if request.method == 'POST':
        schoolid = request.POST.get('schoolid')
        password = request.POST.get('password')

        print(schoolid, password)

        if (db.child("schools").child(schoolid).get()):
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