import os

from app.builders.abstract import AbsTask
from app.builders.builders import ProjectConfig
from app.builders.utils import make_dirs, remove_dirs, create_zip, make_file
from app.builders.templates import flaskenv, gitignore, config, readme, requirements, shell_context, blueprint_init, \
    blueprint_route, app_init, blueprint, quick_script


class BuildDirsTask(AbsTask):
    """Task for make project dirs
    """
    dirs = ['static', 'templates', 'tests']

    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    def _create_user_home(self) -> None:
        """if directory for user f.e. 'alex' is not exists, we first create it,
        which is ./projects/<user>/
        """
        make_dirs(self.config.user_home)

    def _create_project_home(self) -> None:
        """here we make project home, which is ./projects/<user>/<project name>
        """
        make_dirs(self.config.project_home)

    def _create_app_home(self) -> None:
        """here we make app home, which is ./projects/<user>/<project name>/app
        """
        make_dirs(self.config.app_home)

    def execute(self) -> None:
        self._create_user_home()
        self._create_project_home()
        self._create_app_home()

        for directory in self.dirs:
            make_dirs(os.path.join(self.config.app_home, directory))

    def rollback(self) -> None:
        remove_dirs(self.config.project_home)


class BuildConfigsTask(AbsTask):
    """Task for make project configurations
    """
    files = ['.flaskenv', '.gitignore', 'config.py', 'README', 'requirements.txt']
    contents = [flaskenv, gitignore, config, readme, requirements, shell_context]

    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    def _correct_env(self) -> None:
        """
        """
        self.contents[0] = self.contents[0].replace('<app_name>', self.config.project_name)

    def _create_shell_context(self) -> None:
        """just edit the filename of shell context python file, f.e. flasky.py
        """
        self.files.append('{}.py'.format(self.config.project_name))

    def _create_paths(self) -> None:
        """just edit the filepath of configuration files, to place them properly
        """
        self.files = list(map(lambda x: os.path.join(self.config.project_home, x), self.files))

    def execute(self) -> None:
        self._correct_env()
        self._create_shell_context()
        self._create_paths()
        for file, content in zip(self.files, self.contents):
            make_file(file, content)

    def rollback(self) -> None:
        raise NotImplemented


class CreateBlueprintsTask(AbsTask):
    """Task to make blueprint sub-folders in app and templates
    """
    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    def execute(self) -> None:
        for package in self.config.packages:
            init = blueprint_init.replace('<package>', package)
            route = blueprint_route.replace('<package>', package)
            make_dirs(os.path.join(self.config.app_home, package))
            make_file(os.path.join(os.path.join(self.config.app_home, package), '__init__.py'), init)
            make_file(os.path.join(os.path.join(self.config.app_home, package), 'routes.py'), route)

    def rollback(self) -> None:
        raise NotImplemented


class CreateQuickStartScriptTask(AbsTask):
    """Task to make simple sh script which will help you to init venv, install pip packages
    and you can then just run app with `flask run`
    """
    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    def execute(self):
        make_file(os.path.join(self.config.project_home, 'quick.sh'), quick_script)

    def rollback(self):
        raise NotImplemented


class CreateAppInitTask(AbsTask):
    """Task to create main app __init__.py with all packages blueprints
    """
    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    def execute(self) -> None:
        blueprints = ''
        for package in self.config.packages:
            blueprints += blueprint.replace('<package>', package)

        init = app_init.replace('<blueprints>', blueprints)
        make_file(os.path.join(self.config.app_home, '__init__.py'), init)

    def rollback(self) -> None:
        raise NotImplemented


class CreateArchiveTask(AbsTask):
    """Task which creates zip archive from created project
    and return path for it
    """
    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    def execute(self) -> None:
        create_zip(self.config.project_name, self.config.project_home)

    def rollback(self) -> None:
        raise NotImplemented


class DeleteProjectTask(AbsTask):
    """Task which remove project completely
    """
    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    def execute(self) -> None:
        remove_dirs(self.config.project_home)

    def rollback(self) -> None:
        raise NotImplemented
