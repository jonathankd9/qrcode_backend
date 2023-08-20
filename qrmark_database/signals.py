from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Student, Lecturer

# @receiver(post_save, sender=User)
# def create_student_or_lecturer(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_student:
#             Student.objects.create(student=instance)
#         elif instance.is_lecturer:
#             Lecturer.objects.create(lecturer=instance)


@receiver(post_save, sender=User)
def save_student_or_lecturer(sender, instance, **kwargs):
    try:
        # Check if the instance is a student and if a Student object exists
        if instance.is_student and not hasattr(instance, 'student'):
            Lecturer.objects.filter(lecturer=instance).delete()  # Delete any existing lecturer object
            Student.objects.create(student=instance)  # Create a new student object
        # Check if the instance is a lecturer and if a Lecturer object exists
        elif instance.is_lecturer and not hasattr(instance, 'lecturer'):
            Student.objects.filter(student=instance).delete()  # Delete any existing student object
            Lecturer.objects.create(lecturer=instance)  # Create a new lecturer object
    except Student.DoesNotExist:
        Student.objects.create(student=instance)  # Create a new student object if it doesn't exist
    except Lecturer.DoesNotExist:
        Lecturer.objects.create(lecturer=instance)  # Create a new lecturer object if it doesn't exist

