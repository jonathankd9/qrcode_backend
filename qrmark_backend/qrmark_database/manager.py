from django.contrib.auth.models import BaseUserManager

from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        """
        Creates and saves a User with the given user_id and password.
        """
        if not user_id:
            raise ValueError("The User ID must be set")

        if not user_id.isdigit() or len(user_id) != 8:
            raise ValidationError("The User ID must be exactly 8 digits")

        if password is None or len(password) != 5 or not password.isdigit():
            raise ValidationError("The password must be exactly 5 digits")

        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.is_student = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given user_id and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_lecturer", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(user_id, password, **extra_fields)
