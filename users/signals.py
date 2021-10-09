from django.db.models.signals import pre_save
from .models import NewUser
from django.dispatch import receiver
from dashboard.models import Notifications

@receiver(pre_save, sender=NewUser)
def album_pre_save(sender, instance, **kwargs):
    if instance.id is None:
        pass

    else:
        current = instance
        previous = NewUser.objects.get(id=instance.id)
        # Points change
        if previous.points != current.points:
            notif = Notifications()
            notif.message = "Your points increased from " + str(previous.points)+" to "+str(current.points)
            notif.user=instance
            notif.type="Success"
            notif.save()

            if current.points>100:
                # Reached silver
                notif = Notifications()
                notif.message = "Congratualations, you reached Silver level"
                notif.user = instance
                notif.type = "Success"
                notif.save()

            if current.points>1000:
                #Reached Gold
                notif = Notifications()
                notif.message = "Congratualations, you reached Gold level"
                notif.user = instance
                notif.type = "Success"
                notif.save()
        # Referral
        if previous.referrals != current.referrals:
            notif = Notifications()
            notif.message = "Congratualations, someone used your AlcherID to register. Your points are updated"
            notif.user = instance
            notif.type = "Success"
            notif.save()
            

        
