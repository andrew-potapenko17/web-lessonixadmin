from django.shortcuts import redirect

def is_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        # Get the role of user
        schoolid = request.session.get('schoolid')
        
        # If the user is not authenticated, or role is "teacher", redirect to the home page
        if not schoolid:
            print("Not authenticated")
            return redirect('login')
        
        # If checks pass, proceed to the original view
        return view_func(request, *args, **kwargs)
    
    return wrapper