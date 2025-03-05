from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item

@receiver(post_save, sender=Item)
def update_repeatability(sender, instance, **kwargs):
    if instance.repeatID is None:
       instance.repeatability = False
    else:
        instance.repeatability = True
        instance.save()
