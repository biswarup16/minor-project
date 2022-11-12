from django.urls import path
from .views import *

urlpatterns = [
    path('', login , name='login'),
    path('logout/', logout_user , name='logout'),
    path('forgot-password/', forgot_password , name='forgotpassword'),
    path('change-password/<token>/', change_password , name='changepassword'),
    
    # ------------------------------------------------------------------------------------ 
    
    path('register/', register , name='register'),
    path('dashboard/', dashboard , name='dashboard'),
    path('token/', toke_send , name='token'),
    path('success/', success , name='success'),
    path('verify/<auth_token>', verify , name='verify'),
    path('error/', error_page , name='error'),


    # ------------------------------------------------------------------------------------ 

    path('students/', student , name='students'),

    # ------------------------------------------------------------------------------------ 
    
    path('profile/',profile , name='profile'),
    
    # ------------------------------------------------------------------------------------ 
    path('prospectus-payment-verification/',prospectus_success,name="prospectus"),
    
    # ------------------------------------------------------------------------------------ 
    
    path('send-admission-form/',send_admission_form , name='send_admission_form'),
    
    # ------------------------------------------------------------------------------------ 
    path('update-student-detail/<str:username>/',update_student_detail,name='update_student_detail'),
    
    # ------------------------------------------------------------------------------------ 
    path('delete-student/<str:username>/',delete_student,name='delete_student'),
    # ------------------------------------------------------------------------------------ 
    path('upload-document/',upload_document,name='upload_document'),
    
    # -------------------------------------File Management----------------------------------------------- 
    path('files/',view_file,name='view_file'),
    path('upload-file/',upload_file,name='upload_file'),
    
    
    path('under-mantainance/',not_found,name='not_found'),
    
    # ---------------------------------------Print ID Card--------------------------------------------- 
    path('print-id-card/<str:username>/',print_id,name="print_id"),
    
    
    # -------------------------------------Live Search Student----------------------------------------------- 
    
    path('search-student/',search_student,name="search_student"),
    
    # -------------------------------------Selected Students-----------------------------------------------
    
    path('selected-students/',selected_students,name="selected_students"),
    
    path('selected-students-details/<str:id>',selected_students_details,name="selected_students_details"),
    
    # -------------------------------------Notice -----------------------------------------------
    
    path('upload-notice/',upload_notice,name="upload_notice"),
    
    path('view-all-notices/',all_notice,name="all_notice")
     
    

    
] 