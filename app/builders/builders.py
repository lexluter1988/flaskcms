import json
import os
import re
from uuid import uuid4
from flask import current_app

from app.builders.abstract import AbsTask, AbsPipeline


class ProjectConfig:
    """Project configuration class, contains root directory path, name and unique uuid for project
    """
    def __init__(self, owner, name, packages='main, auth'):
        self.user = owner
        self.project_name = name
        self.uuid = uuid4()

        self.user_home = os.path.join(current_app.config['PROJECTS_ROOT'], owner)
        self.project_home = os.path.join(self.user_home, name)
        self.app_home = os.path.join(self.project_home, 'app')
        self.archive = os.path.join(current_app.config['ARCHIVE_FOLDER'], name + '.' + 'zip')

        self.packages = re.findall(r'\w\w+', packages)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class BuildProject(AbsPipeline):
    """Builder of project, pipeline of tasks
    """
    def __init__(self, config):
        self.config = config
        self.tasks = []

    def task_add(self, task: AbsTask):
        self.tasks.append(task)

    def task_remove(self, task):
        self.tasks.remove(task)

    def run_pipeline(self):
        for task in self.tasks:
            task.execute()
