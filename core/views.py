from calendar import month_name
from operator import imod
import os
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login as auth_login, logout
from django.contrib.auth.decorators import login_required
import razorpay
from adbu.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def login(request):
    if request.method == 'POST':
       username = request.POST.get('username') 
       password = request.POST.get('password') 
       
       if len(username) and len(password) != 0:
           user_obj = User.objects.filter(username = username).first()
           if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('/')
           profile_obj = Profile.objects.filter(user = user_obj ).first()
           if not profile_obj.is_verified:
                messages.success(request, 'Profile is not verified check your mail.')
                return redirect('/')
           user = authenticate(username = username , password = password)
           if user is None:
               messages.success(request, 'Wrong password.')
               return redirect('/')
           auth_login(request, user)
           return redirect('/dashboard')
       
       messages.success(request, 'Please fill your credentials')
       
    return render(request,'auth/login.html')

def logout_user(request):
    logout(request)
    messages.success(request,'You Were Logged Out')
    return redirect('/')

def forgot_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')  
            
            if not User.objects.filter(username=username).first():
                messages.success(request,'User Not Found With This Username')  
                return redirect('/forgot-password')
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            send_forgot_password_mail(user_obj.email ,token)
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.auth_token = token
            profile_obj.save()
            messages.success(request,'An email is sent')  
            return redirect('/forgot-password')
    
    except Exception as e:
        print(e)
    return render(request,'auth/forgotpassword.html')


# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------


def send_forgot_password_mail(email, token):
    subject = 'Your Forgot Password Link'
    message = f''' Hi, click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------

def change_password(request,token):
    context = {}
    try:
        profile_obj = Profile.objects.get(auth_token = token)
        print(profile_obj.user)
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmpassword')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
            
            if  password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, 'Your Password Has Been Changed')
            return redirect('/')
             
    except Exception as e:
        print(e)   
         
    return render(request,'auth/changepassword.html',context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(username) and len(first_name) and len(last_name) and len(email) and len(password) != 0:
            
            try:
                if User.objects.filter(username = username).first():
                    messages.error(request,"Username is already taken")
                    return redirect('/register')
            
                if User.objects.filter(email = email).first():
                    messages.error(request,"Email is already taken")
                    return redirect('/register')

                user_obj = User.objects.create(username = username, email = email)    
                user_obj.set_password(password)
                user_obj.save()
                auth_token = str(uuid.uuid4())

                profile_obj = Profile.objects.create(user = user_obj,first_name = first_name, last_name = last_name, auth_token = auth_token)
                profile_obj.save()
                
                prospectus_obj = Prospectus.objects.create(user = user_obj, paid = False)
                prospectus_obj.save()
                
                send_mail_after_refistration(email,auth_token)
                return redirect('/token')

            except Exception as e:
                print(e) 
        messages.error(request,"Please fill the informations")

    return render(request,'auth/register.html')    


@login_required(login_url='/')
def dashboard(request):
    user = request.user
    
    profile_obj = Profile.objects.get(user = user)
   
    prospectus = Prospectus.objects.get(user = user)
    # if AdmissionForm.objects.filter(user = user) is not None:
    #     admission_form = AdmissionForm.objects.filter(user = user)
    #     print(admission_form)
    # else:
    #     admission_form = None 
    
    admission_query = AdmissionForm.objects.filter(user = user).first()
    if admission_query is not None:
        admission_form = 'True'
    else:
        admission_form = 'False'   
       
    
    # admission_form = AdmissionForm.objects.get(user = user)
    # print(admission_query.user)
    
    if  request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        order_amount = 60000
        order_currency = "INR"
        client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
        payment = client.order.create(dict(amount=order_amount, currency= order_currency,payment_capture=1))
        order_id = payment['id']
        prospectus = Prospectus(id=prospectus.id,user_id = prospectus.user_id,first_name=first_name,last_name=last_name,email=email,phone=phone,order_id=order_id)
        prospectus.save()
    
    
    
        if prospectus is not None:
            context ={
                'api_key':RAZORPAY_API_KEY,
                'order_amount':order_amount,
                'currency':order_currency,
                'order_id':order_id,'profile_obj':profile_obj,'prospectus':prospectus,'payment':payment
            }
        return render(request,'dashboard/dashboard.html',context)  
    
    
    
    return render(request,'dashboard/dashboard.html',{'profile_obj':profile_obj,'user':user,'prospectus':prospectus,'admission_form':admission_form,'admission_query':admission_query})    

# ------------------------Email Verification Code----------------------------  

def success(request):
    return render(request,'auth/success.html')

def toke_send(request):
    return render(request,'auth/token_send.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified == True:
                messages.success(request,"You account is already verified")
                return redirect('/')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,"You Have Successfully Verified")
            return redirect('/')
        else:
            return redirect('/error')    
    except Exception as e:
        print(e)   

def error_page(request):
    return render(request,'auth/error.html')             

def send_mail_after_refistration(email,token):
    subject = "Your need's To Be verified"
    message = f'Hii click the to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    
    
# ---------------------------Student Details------------------------------------    

@login_required(login_url='/')
def student(request):
    profile_obj = Profile.objects.all().exclude(user=request.user)
    user_obj = User.objects.all().exclude(username=request.user)
    zippedList = zip(profile_obj,user_obj)
    return render(request,'dashboard/student.html',{'profile_obj': zippedList})


# ---------------------------Profile Details----------------------------------------

@login_required(login_url='/')
def profile(request):
    user = request.user
    profile_data = Profile.objects.get(user=user)
    
    if request.method == 'POST':
        if len(request.FILES) != 0:
            # if len(profile_data.profile_pic) > 0:
                # os.remove(profile_data.profile_pic.path)
            profile_data.profile_pic = request.FILES['profile']
        # if 'image' in request.FILES:
        # profile = request.FILE['profile']
        profile_data.save()
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        
        # user_obj = User.objects.all().filter(email=email)
        # print(user_obj)
        
       
        user_data = User.objects.filter(username=user).update(first_name=first_name,last_name=last_name,email=email)
        return redirect('/profile/')
    return render(request,'dashboard/profile.html')


# -----------------------------Admission Form Payment -----------------------------
@csrf_exempt
@login_required(login_url='/')
def prospectus_success(request):
    response = request.POST
    print(response)
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    # client instance
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    try:
        status = client.utility.verify_payment_signature(params_dict)
        prospectus = Prospectus.objects.get(order_id=response['razorpay_order_id'])
        prospectus.razorpay_payment_id = response['razorpay_payment_id']
        prospectus.paid = True
        prospectus.save()
        messages.success(request,"You Have Successfully Paid")
        return redirect('/dashboard/')
        # return render(request, 'payment_status.html', {'status': True})
    except:
        return render(request,'dashboard/dashboard.html')
    
    
# -----------------------------------Send Admission Form -------------------------------

def send_admission_form(request):
    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_number = request.POST.get('father_number')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_number = request.POST.get('mother_number')
        garduian_name = request.POST.get('garduian_name')
        garduian_number = request.POST.get('garduian_number')
        nationality = request.POST.get('nationality')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        blood_group = request.POST.get('blood_group')
        caste = request.POST.get('caste')
        religion = request.POST.get('religion')
        
        hslc_board = request.POST.get('hslc_board')
        hslc_passing_year = request.POST.get('hslc_passing_year')
        hslc_reg = request.POST.get('hslc_reg')
        hslc_roll = request.POST.get('hslc_roll')
        hslc_total_marks = request.POST.get('hslc_total_marks')
        hslc_marks = request.POST.get('hslc_marks')
        hslc_percentage = request.POST.get('hslc_percentage')
        hslc_school = request.POST.get('hslc_school')
        
        
        hsslc_board = request.POST.get('hsslc_board')
        hsslc_stream = request.POST.get('hsslc_stream')
        hsslc_passing_year = request.POST.get('hsslc_passing_year')
        hsslc_reg = request.POST.get('hsslc_reg')
        hsslc_roll = request.POST.get('hsslc_roll')
        hsslc_percentage = request.POST.get('hsslc_percentage')
        hsslc_school = request.POST.get('hsslc_school')
        
        graduation_course_name = request.POST.get('graduation_course_name')
        graduation_board = request.POST.get('graduation_board')
        graduation_course_type = request.POST.get('graduation_course_type')
        graduation_year = request.POST.get('graduation_year')
        graduation_reg = request.POST.get('graduation_reg')
        graduation_roll = request.POST.get('graduation_roll')
        graduation_total_marks = request.POST.get('graduation_total_marks')
        graduation_marks = request.POST.get('graduation_marks')
        graduation_percentage = request.POST.get('graduation_percentage')
        graduation_university = request.POST.get('graduation_university')
        
        post_graduation_course_name = request.POST.get('post_graduation_course_name')
        post_graduation_board = request.POST.get('post_graduation_board')
        post_graduation_course_type = request.POST.get('post_graduation_course_type')
        post_graduation_year = request.POST.get('post_graduation_year')
        post_graduation_reg = request.POST.get('post_graduation_reg')
        post_graduation_roll = request.POST.get('post_graduation_roll')
        post_graduation_total_marks = request.POST.get('post_graduation_total_marks')
        post_graduation_marks = request.POST.get('post_graduation_marks')
        post_graduation_percentage = request.POST.get('post_graduation_percentage')
        post_graduation_university = request.POST.get('post_graduation_university')
        
        admission_form = AdmissionForm(user=user,full_name=full_name,father_name=father_name,father_occupation=father_occupation,father_number=father_number,mother_name=mother_name,mother_occupation=mother_occupation,mother_number=mother_number,garduian_name=garduian_name,garduian_number=garduian_number,nationality=nationality,dob=dob,gender=gender,blood_group=blood_group,caste=caste,religion=religion,hslc_board=hslc_board,hslc_passing_year=hslc_passing_year,hslc_reg=hslc_reg,hslc_roll=hslc_roll,hslc_total_marks=hslc_total_marks,hslc_marks=hslc_marks,hslc_percentage=hslc_percentage,hsslc_school=hsslc_school,hsslc_board=hsslc_board,hsslc_stream=hsslc_stream,hsslc_passing_year=hsslc_passing_year,hsslc_reg=hsslc_reg,hsslc_roll=hsslc_roll,hsslc_percentage=hsslc_percentage,graduation_course_name=graduation_course_name,graduation_board=graduation_board,graduation_course_type=graduation_course_type,graduation_year=graduation_year,graduation_reg=graduation_reg,graduation_roll=graduation_roll,graduation_total_marks=graduation_total_marks,graduation_marks=graduation_marks,graduation_percentage=graduation_percentage,graduation_university=graduation_university,post_graduation_course_name=post_graduation_course_name,post_graduation_board=post_graduation_board,post_graduation_course_type=post_graduation_course_type,post_graduation_year=post_graduation_year,post_graduation_reg=post_graduation_reg,post_graduation_roll=post_graduation_roll,post_graduation_total_marks=post_graduation_total_marks,post_graduation_marks=post_graduation_marks,post_graduation_percentage=post_graduation_percentage,post_graduation_university=post_graduation_university)
        admission_form.save()
        messages.success(request, 'Successfully Submitted Admission Form.')
    else:
        messages.error(request, 'Please Fill The Fill Up The Form Correctly')
        
    return redirect('/dashboard/')   


# -----------------------------------Update Student Details -------------------------------
 
def update_student_detail(request,username):
    user_obj = User.objects.get(username=username)
    profile_obj = Profile.objects.get(user=user_obj.id)
    
    if request.method == 'POST':
        if len(request.FILES) != 0:
            # if len(profile_data.profile_pic) > 0:
                # os.remove(profile_data.profile_pic.path)
            profile_obj.profile_pic = request.FILES['profile']
        # if 'image' in request.FILES:
        # profile = request.FILE['profile']
        profile_obj.save()
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        
        # user_obj = User.objects.all().filter(email=email)
        # print(user_obj)
        
       
        user_data = User.objects.filter(username=username).update(first_name=first_name,last_name=last_name,email=email)
        return redirect(request.path_info)
    return render(request,'dashboard/update-student-detail.html',{'profile_obj':profile_obj,'user_obj':user_obj})
    

def delete_student(request,username):
    user_obj = User.objects.filter(username=username)
    query = user_obj.delete()
    if query:
        return redirect('/students/')
    
        