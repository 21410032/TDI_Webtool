from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class Profile(AbstractUser):

    username = None
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    objects = UserManager()

    def __str__(self):
        return self.email
    


