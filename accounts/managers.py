from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_useer(self, phone_number, password = None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number required")
        
        extra_fields['email'] = self.normalize_email(extra_fields['email'])

        user = self.model(phone_number = phone_number, **extra_fields)

        user.set_password(password)
        user.save(using = self.db)

        return user