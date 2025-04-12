from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import cfg
from . import generator
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

@is_authenticated
def addClassPage(request):
    if request.method == 'POST':
        class_digit = request.POST.get('class')
        class_letter = request.POST.get('letter')
        leadteacher = request.POST.get('leadteacher')

        schoolid = request.session.get('schoolid')
        students_list = request.session.get('students', [])

        try:
            class_name = f"{str(class_digit)}-{str(class_letter)}"

            student_ids = []
            for full_name in students_list:
                student_id = generator.unic(k=10)
                student_ids.append(student_id)
                
                registration_code = generator.unic(k=16)

                db.child("registercodes").child(registration_code).set({
                    "student_id": student_id,
                    "class": class_name,
                    "schoolID": schoolid
                })

                db.child("students").child(schoolid).child(student_id).set({
                    "full_name": full_name,
                    "registered": False,
                    "registercode": registration_code,
                    "schoolStatus": "nolesson",
                    "studentStatus": "outschool",
                    "class": class_name,
                })

            db.child("school_classes").child(schoolid).child(class_name).set({
                "class": class_digit,
                "letter": class_letter,
                "leadTeacher": leadteacher,
                "students": student_ids 
            })
            
            request.session['students'] = []
            
            return redirect('classes')
        except Exception as e:
            return redirect('addclass')

    return render(request, 'adminpanel/addclass.html')

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