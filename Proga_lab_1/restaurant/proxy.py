from .models import Client, Administrator


class UserProxy:

    def __init__(self, pk=None, login=None, password=None, admin=False):
        self._user = None
        self._admin = False
        if pk:
            self._user = Administrator.objects.get(pk=pk) \
                        if admin \
                        else Client.objects.get(pk=pk)
        if login or password:
            kwargs = {}

            kwargs.__setitem__('login', login) if login else None
            kwargs.__setitem__('password', password) if password else None

            try:
                self._user = Administrator.objects.get(**kwargs)
                self._admin = True
            except Administrator.DoesNotExist:
                self._user = Client.objects.get(**kwargs)

    def get_id(self):
        if self._user:
            return self._user.id

    def get_login(self):
        if self._user:
            return self._user.login

    def get_password(self):
        if self._user:
            return self._user.password

    def is_admin(self):
        return self._admin

    def get_user(self):
        return self._user
