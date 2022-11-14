from .models import Settings,Profile


def available(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated == True:
        user = request.user
        return {
            # iteConfig.objects.first()
            
            # "profile_obj": 
            'setting':Settings.objects.get(),
            "profile_obj1": Profile.objects.get(user = user)

        }
    else:
        return {
            # iteConfig.objects.first()
            'setting':Settings.objects.get()
            
            # "profile_obj": 
            # "profile_obj1": Profile.objects.get(user = user)

        }
            