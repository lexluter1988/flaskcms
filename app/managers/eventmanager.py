from app import db
from app.models import Event


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


class Action:
    @staticmethod
    def project_created(project: str):
        return f'user created new project {project}'

    @staticmethod
    def project_removed(project: str):
        return f'user removed project {project}'

    @staticmethod
    def user_registered():
        return f'new user registered'

    @staticmethod
    def user_logged_in():
        return f'user logged in'

    @staticmethod
    def user_logged_out():
        return f'user logged out'


@singleton
class EventManager:
    @staticmethod
    def send(user, action: str):
        event = Event(author=user, action=action)
        db.session.add(event)
        db.session.commit()

    def clear(self):
        pass

    def get_by_method(self, method):
        pass
