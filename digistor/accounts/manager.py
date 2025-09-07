from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, first_name=None, last_name=None, password=None):
        """
        """
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone_number=phone_number,
            email=email or '',
            first_name=first_name or '',
            last_name=last_name or ''
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name, password):
        user = self.create_user(phone_number, email,
                                first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
