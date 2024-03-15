# manager.py
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        #normalize means convert in lower case
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        #for set the password for user
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, password=None, **kwargs):
    #     kwargs.setdefault('is_staff', True)
    #     kwargs.setdefault('is_superuser', True)

    #     if kwargs.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if kwargs.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self.create_user(email, password, **kwargs)
