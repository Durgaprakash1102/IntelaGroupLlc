from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


User = get_user_model()


class MultiFieldAuthenticationBackend(ModelBackend):

    def authenticate(
        self,
        request,
        username=None,
        password=None,
        **kwargs
    ):

        identifier = username

        if not identifier or not password:
            return None

        identifier = identifier.strip()

        try:

            user = User.objects.get(
                Q(username__iexact=identifier)
                | Q(email__iexact=identifier)
                | Q(phone_number=identifier)
            )

        except User.DoesNotExist:
            return None

        except User.MultipleObjectsReturned:
            return None

        if user.check_password(password):

            if self.user_can_authenticate(user):
                return user

        return None