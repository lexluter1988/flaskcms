from functools import wraps

from flask import url_for, flash
from flask_babel import gettext as _
from flask_login import current_user
from werkzeug.utils import redirect


def permissions_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                flash(_('Insufficient permissions!'))
                return redirect(url_for('main.index'))
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance
