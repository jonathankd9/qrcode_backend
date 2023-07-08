from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Student, Lecturer

@receiver(post_save, sender=User)
def create_student_or_lecturer(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            Student.objects.create(student=instance)
        elif instance.is_lecturer:
            Lecturer.objects.create(lecturer=instance)

# @receiver(post_save, sender=User)
# def save_student_or_lecturer(sender, instance, **kwargs):
#     if instance.is_student:
#         try:
#             instance.save()
#         except Student.DoesNotExist:
#             Student.objects.create(student=instance)
#     elif instance.is_lecturer:
#         try:
#             instance.save()
#         except Lecturer.DoesNotExist:
#             Lecturer.objects.create(lecturer=instance)
