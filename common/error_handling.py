
class AppErrorBaseClass(Exception):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass


class NotAllowed(AppErrorBaseClass):
    pass


class NotReady(AppErrorBaseClass):
    pass