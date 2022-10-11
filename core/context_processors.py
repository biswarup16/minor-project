from .models import *


def available(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated == True:
        user = request.user
        print(user)
        return {
            # iteConfig.objects.first()
            
            # "profile_obj": 
            "profile_obj1": Profile.objects.get(user = user)

        }
    else:
        return {
            # iteConfig.objects.first()
            
            # "profile_obj": 
            # "profile_obj1": Profile.objects.get(user = user)

        }
            