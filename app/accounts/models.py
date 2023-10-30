from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    """
    Manager for the user Model
    """

    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
    ):
        if not email:
            raise ValueError("Email can't be blank!")
        if not first_name:
            raise ValueError("First name can't be blank!")
        if not last_name:
            raise ValueError("Last name can't be blank!")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name.lower(),
            last_name=last_name.lower(),
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        password=None,
    ):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)

        # create Permissions on superuser create
        return user


class User(AbstractBaseUser):
    """custom Model of the users"""

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def save(self, *args, **kwargs):
        """in save i make the first and last name lower for better store"""
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        return super().save(*args, **kwargs)

    @property
    def full_name(self):
        """return the first and the last name in title format"""
        return f"{self.first_name} {self.last_name}".title()

    def __str__(self):
        """return the email"""
        return self.email

    def has_module_perms(self, app_label):
        """only admin can enter to the admin panel"""
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """only admin can enter to the admin panel"""
        return self.is_admin
