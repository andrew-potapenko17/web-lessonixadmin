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
        students_list = request.POST.getlist('students')
        print(students_list)
        #students_list = request.session.get('students', [])
        
        try:
            print(" Test #1")
            class_name = f"{str(class_digit)}-{str(class_letter)}"

            student_ids = []
            for full_name in students_list:
                student_id = generator.unic(length=10)
                student_ids.append(student_id)

                registration_code = generator.unic(length=16)

                print(" Test #2")

                db.child("registercodes").child(registration_code).set({
                    "student_id": student_id,
                    "class": class_name,
                    "schoolID": schoolid
                })

                print(" Test #3")

                db.child("students").child(schoolid).child(student_id).set({
                    "full_name": full_name,
                    "registered": False,
                    "registercode": registration_code,
                    "schoolStatus": "nolesson",
                    "studentStatus": "outschool",
                    "class": class_name,
                })

            print(" Test #4")

            db.child("school_classes").child(schoolid).child(class_name).set({
                "class": class_digit,
                "letter": class_letter,
                "leadTeacher": leadteacher,
                "students": student_ids 
            })
            
            request.session['students'] = []
            
            return redirect('classes')
        except Exception as e:
            print(e)
            return redirect('addclass')

    return render(request, 'adminpanel/addclass.html')

@is_authenticated
def staffPage(request):
    schoolid = request.session.get('schoolid')
    staff_list = []
    staff_list_inactive = []

    try:
        users = db.child("users").get().val()
        if users:
            staff_list = [
                {
                    'full_name': user_info.get('full_name', 'N/A'),
                    'user_id': user_id,
                    'primaryclass': user_info.get('primaryclass', 'N/A'),
                    'role': user_info.get('role', 'N/A'),
                }
                for user_id, user_info in users.items()
                if user_info.get('school_id') == schoolid and user_info.get('role') != 'student'
            ]
    except Exception as e:
        print(f"Failed to retrieve users. Error: {str(e)}")

    try:
        codes = db.child("personalregistercodes").get().val()
        if codes:
            staff_list_inactive = [
                {
                    'full_name': info.get('full_name', 'N/A'),
                    'register_code': code,
                    'primaryclass': info.get('primary', 'N/A'),
                    'role': info.get('role', 'N/A'),
                }
                for code, info in codes.items()
                if info.get('school_id') == schoolid
            ]
    except Exception as e:
        print(f"Failed to retrieve personalregistercodes. Error: {str(e)}")

    return render(
        request,
        'adminpanel/staff.html',
        context={
            'staff_list': staff_list,
            'staff_list_inactive': staff_list_inactive,
        },
    )


@is_authenticated
def addStaffPage(request, type):
    if request.method == 'POST':
        full_name = request.POST.get('teacherName')
        schoolid = request.session.get('schoolid')

        if not db.child('schools').child(schoolid).get().val():
            print(request, "Invalid school ID")
            return redirect('register_personnel')

        register_code = generator.unic(7)

        try:
            if type == "teacher":
                primary = request.POST.get('primaryClass', '')
                subjects = request.POST.get('subjects', '')
                rooms = request.POST.get('rooms', '')

                subjects_dict = {s.strip(): s.strip() for s in subjects.split(',') if s.strip()}
                rooms_dict = {r.strip(): r.strip() for r in rooms.split(',') if r.strip()}

                data = {
                    "full_name": full_name,
                    "school_id": schoolid,
                    "role": type,
                    "subjects": subjects_dict,
                    "cabs": rooms_dict,
                }

                if primary:
                    data["primary"] = primary

                db.child('personalregistercodes').child(str(register_code)).set(data)  

            elif type == "med":
                db.child('personalregistercodes').child(str(register_code)).set({
                    "full_name": full_name,
                    "school_id": schoolid,
                    "role": type,
                })

            return redirect('staff')

        except Exception as e:
            return redirect('staff')
        
    if type == "teacher":
        return render(request, 'adminpanel/addteacher.html')
    elif type == "med":
        return render(request, 'adminpanel/addmed.html')


@is_authenticated
def staffProfile(request, stringid: str):
    schoolid = request.session.get('schoolid')

    context = {}

    if len(stringid) == 7:
        staff_data = db.child("personalregistercodes").child(stringid).get().val()
        if not staff_data or staff_data.get('school_id') != schoolid:
            return HttpResponse("Invalid or unauthorized access to inactive staff profile.", status=403)
        
        context.update({
            "full_name": staff_data.get("full_name", "N/A"),
            "role": staff_data.get("role", "N/A"),
            "registercode": stringid,
            "primary": staff_data.get("primary", "N/A"),
            "subjects": staff_data.get("subjects", {}),
            "rooms": staff_data.get("cabs", {}),
        })

    else:
        staff_data = db.child("users").child(stringid).get().val()
        if not staff_data or staff_data.get('school_id') != schoolid:
            return HttpResponse("Invalid or unauthorized access to staff profile.", status=403)

        context.update({
            "full_name": staff_data.get("full_name", "N/A"),
            "role": staff_data.get("role", "N/A"),
            "primary": staff_data.get("primary", "N/A"),
            "subjects": staff_data.get("subjects", {}),
            "rooms": staff_data.get("cabs", {}),
        })

    return render(request, 'adminpanel/staffprofile.html', context)


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