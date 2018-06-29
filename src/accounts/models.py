from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import pre_save, post_save

from django.conf import settings
from  django.core.validators import RegexValidator


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

USERNAME_REGEX = '^[A-Za-z0-9.@+-]+$'

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, validators=[
      RegexValidator(
        regex=USERNAME_REGEX,
        message='Username has to be alphanumeric or contains .@+-',
        code = 'invalid_username' 
      )
    ], unique = True
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    zipcode = models.CharField(default='97204', max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        # return self.is_admin



# extend user model
class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  city = models.CharField(max_length=120, blank=True, null=True)

  def __init__(self):
    return str(self.user.username)

def post_save_user_model_receiver(sender, instance,created, *args, **kwargs):
    if created:
      try:
        Profile.objects.create(instance=user)
      except:
        pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)  