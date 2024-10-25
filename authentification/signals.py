from django.db.models.signals import pre_delete
from django.dispatch import receiver
from authentification.models import CustomUser, SomeOtherModel

@receiver(pre_delete, sender=CustomUser)
def delete_related_objects(sender, instance, **kwargs):
    # Delete related objects here
    SomeOtherModel.objects.filter(user=instance).delete()
    # Add other related models as needed...
