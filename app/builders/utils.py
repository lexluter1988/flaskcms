import shutil
from os import makedirs, remove

from flask import current_app


def make_file(path, content):
    try:
        with open(path, 'w') as f:
            f.write(content)
    except OSError:
        pass


def remove_file(filename):
    try:
        remove(filename)
    except OSError as e:
        print(e)


def make_dirs(dir_name):
    try:
        makedirs(dir_name)
    except OSError:
        pass


def remove_dirs(dir_name):
    try:
        shutil.rmtree(dir_name)
    except OSError as e:
        print(e)


def create_zip(project_name, project_home):
    try:
        shutil.make_archive(
            base_name='{}/{}'.format(current_app.config['ARCHIVE_FOLDER'], project_name),
            format='zip',
            root_dir=project_home)
        return project_home + '/' + project_name + '.zip'
    except OSError:
        pass