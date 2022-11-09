from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile')
    is_verified = models.CharField(max_length=10,default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Prospectus(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    first_name = models.CharField(default=" ",max_length=50,null=True,blank=True)
    last_name = models.CharField(default=" ",max_length=50,null=True,blank=True)   
    email = models.CharField(default=" ",max_length=50,) 
    phone = models.CharField(default=" ",max_length=12,null=True,blank=True) 
    order_id = models.CharField(default=" ",max_length=100,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    
    
    paid = models.CharField(max_length=10,default=False)
    
    def __str__(self):
        return str(self.user)
    

IS_VERIFIED = [
    ('True', 'True'),
    ('False', 'False'),
]

class AdmissionForm(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    father_occupation = models.CharField(max_length=200)
    father_number = models.CharField(max_length=17)
    mother_name = models.CharField(max_length=200)
    mother_occupation = models.CharField(max_length=200)
    mother_number = models.CharField(max_length=17)
    garduian_name = models.CharField(max_length=200)
    garduian_number = models.CharField(max_length=17)
    nationality = models.CharField(max_length=17)
    dob = models.CharField(max_length=17)
    gender = models.CharField(max_length=17)
    blood_group = models.CharField(max_length=17)
    caste = models.CharField(max_length=17)
    religion = models.CharField(max_length=17)
    
    course = models.CharField(max_length=30,default=" ",null=True,blank=True)
    
    
    hslc_board = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hslc_passing_year = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hslc_reg = models.CharField(max_length=70,default=" ",null=True,blank=True)
    hslc_roll = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hslc_total_marks = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hslc_marks = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hslc_percentage = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hslc_school = models.CharField(max_length=17,default=" ",null=True,blank=True)
    
    
    hsslc_board = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hsslc_stream = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hsslc_passing_year = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hsslc_reg = models.CharField(max_length=70,default=" ",null=True,blank=True)
    hsslc_roll = models.CharField(max_length=70,default=" ",null=True,blank=True)
    hsslc_percentage = models.CharField(max_length=17,default=" ",null=True,blank=True)
    hsslc_school = models.CharField(max_length=17,default=" ",null=True,blank=True)
    
    graduation_course_name = models.CharField(max_length=50,default=" ",null=True,blank=True)
    graduation_board = models.CharField(max_length=50,default=" ",null=True,blank=True)
    graduation_course_type = models.CharField(max_length=17,default=" ",null=True,blank=True)
    graduation_year = models.CharField(max_length=17,default=" ",null=True,blank=True)
    graduation_reg = models.CharField(max_length=70,default=" ",null=True,blank=True)
    graduation_roll = models.CharField(max_length=70,default=" ",null=True,blank=True)
    graduation_total_marks = models.CharField(max_length=17,default=" ",null=True,blank=True)
    graduation_marks = models.CharField(max_length=17,default=" ",null=True,blank=True)
    graduation_percentage = models.CharField(max_length=17,default=" ",null=True,blank=True)
    graduation_university = models.CharField(max_length=50,default=" ",null=True,blank=True)
    
    post_graduation_course_name = models.CharField(max_length=50,default=" ",null=True,blank=True)
    post_graduation_board = models.CharField(max_length=50,default=" ",null=True,blank=True)
    post_graduation_course_type = models.CharField(max_length=17,default=" ",null=True,blank=True)
    post_graduation_year = models.CharField(max_length=17,default=" ",null=True,blank=True)
    post_graduation_reg = models.CharField(max_length=70,default=" ",null=True,blank=True)
    post_graduation_roll = models.CharField(max_length=70,default=" ",null=True,blank=True)
    post_graduation_total_marks = models.CharField(max_length=17,default=" ",null=True,blank=True)
    post_graduation_marks = models.CharField(max_length=17,default=" ",null=True,blank=True)
    post_graduation_percentage = models.CharField(max_length=17,default=" ",null=True,blank=True)
    post_graduation_university = models.CharField(max_length=50,default=" ",null=True,blank=True)
    
    is_verified = models.CharField(max_length=10,
        choices=IS_VERIFIED,
        default=False)
    
    
    def __str__(self):
        return self.full_name
    
    
class AdmissionDocument(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    hslc_doc = models.ImageField(upload_to='AdmissionDocument')
    hslc_marksheet = models.ImageField(upload_to='AdmissionDocument')
    hsslc_doc = models.ImageField(upload_to='AdmissionDocument')
    hsslc_marksheet = models.ImageField(upload_to='AdmissionDocument')
    caste_certificate = models.ImageField(upload_to='AdmissionDocument')


    class Meta:
        verbose_name = ("AdmissionDocument")
        verbose_name_plural = ("AdmissionDocuments")

    def __str__(self):
        return str(self.user)

    
# -------------------------------- File Upload Models ----------------------------------    

class UploadFile(models.Model):
    title = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = ("Upload File")
        verbose_name_plural = ("Upload Files")

    def __str__(self):
        return self.title

# ----------------------------------------Settings-----------------------------------------
class Settings(models.Model):
    name = models.CharField('Name of the Institution',max_length=255, blank=True,null=True)
    logo = models.ImageField('Logo',upload_to='Logo', blank=True,null=True)
    favicon = models.ImageField('Favicon',upload_to='Logo', blank=True,null=True)
    address = models.TextField('Address', blank=True,null=True)
    pin_code = models.CharField('Pin Code',max_length=6, blank=True,null=True)
    phone1 = models.CharField('Contact Number 1',max_length=12, blank=True,null=True)
    phone2 = models.CharField('Contact Number 2',max_length=12, blank=True,null=True)
    class Meta:
        verbose_name = ("Setting")
        verbose_name_plural = ("Settings")
    def __str__(self):
        return str(self.name)    
    

  
    

   
    
    
   

    
    