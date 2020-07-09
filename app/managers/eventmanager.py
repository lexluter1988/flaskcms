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
    def project_created(user: str, project: str):
        return f'user {user} created new project {project}'

    @staticmethod
    def project_removed(user: str, project: str):
        return f'user {user} removed project {project}'

    @staticmethod
    def user_registered(user: str):
        return f'new user {user}'

    @staticmethod
    def user_logged_in(user: str):
        return f'user {user} logged in'

    @staticmethod
    def user_logged_out(user: str):
        return f'user {user} logged out'


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
