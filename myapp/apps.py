from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        # Makes sure all signal handlers are connected
        from myapp import handler  # noqa
