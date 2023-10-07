from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib import messages
import bcrypt
import csv


# Create your views here.
def index(request):
    return render (request, 'auths/authentication.html')

def authentication(request):
    if request.method == "POST":       
        name = request.POST.get('name')
        email = request.POST.get('email')
        passwd = request.POST.get('password')
        
        if name is not None:
            # Sign up
            # existing_users_psno = userinfo.objects.filter(psno = psno)
            existing_users_email = userinfo.objects.filter(email = email)
            if len(existing_users_email) != 0:
                messages.error(request, 'Email id already exists')
                return redirect('auths:index')
            else:
                password = passwd.encode('utf-8')    # the password to hash, encoded as bytes        
                salt = bcrypt.gensalt()   # generate a salt to add to the password before hashing        
                hashed_password = bcrypt.hashpw(password, salt)    # hash the password with the salt using the bcrypt hash function  
                        
                obj = userinfo(name = name, email = email, password = hashed_password) # Adding the new user to the database
                obj.save()
                
                # creating QnA csv for each new users
                file_name = "./media/user/QnA/"+email+".csv"
                with open(file_name, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    # add header
                    csv_writer.writerow(['Question', 'Answer', 'Source', 'Page', 'Line'])
                    
                messages.success(request, 'Successfully Register')
                return redirect('auths:index')
                        
        else:
            # sign in
            curr_user = userinfo.objects.filter(email = email)
            # checking if the username exists or not in the database
            if len(curr_user) == 0:
                messages.error(request, 'Invalid Username')
                return redirect('auths:index')
            else:
                authenticated_user = check_pass(curr_user, passwd.encode('utf-8'))
                if authenticated_user is not None:
                    request.session['user_email'] = authenticated_user.email
                    messages.success(request, 'Logged in successfully')
                    return redirect('user:upload_files')
                else:
                    messages.error(request, 'Invalid Password')
                    return redirect('auths:index')
            
    else:  
        return redirect('auths:index')
    

def check_pass(curr_user, entered_passwd):
    '''This function will take the credentials given by the user and will check in the database.
    It will return the current user object if verified else None object.'''
    
    # if user is present in the database --> checks the password and then 
    if bcrypt.checkpw(entered_passwd, curr_user[0].password):
        return curr_user[0]


def logout(request):
    '''This function logs out the session of the current user
    And also deletes the current session'''
    user_email = request.session.get('user_email')
    # Deleting the session of the current user
    del request.session['user_email']
    messages.success(request, 'Logged Out')
    return redirect('auths:index')


