from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import UserProfile
from student.models import Student
from enrollment.models import Enroll
from payment.models import Payment


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)


# Utility function to get school from user
def get_user_school(user):
    try:
        return user.userprofile.school
    except UserProfile.DoesNotExist:
        return None


# Signal to auto-assign school on save if model has created_by
@receiver(pre_save, sender=Student)
@receiver(pre_save, sender=Enroll)
@receiver(pre_save, sender=Payment)
def set_school_on_save(sender, instance, **kwargs):
    if not instance.pk and hasattr(instance, 'created_by'):
        user = instance.created_by
        if not user.is_superuser:
            school = get_user_school(user)
            if school:
                instance.school = school
