from flask import url_for, redirect, render_template
from flask_login import current_user

from app.builders.builders import ProjectConfig, BuildProject
from app.builders.tasks import BuildDirsTask, CreateArchiveTask, BuildConfigsTask, DeleteProjectTask, \
    CreateBlueprintsTask, CreateAppInitTask, CreateQuickStartScriptTask
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/base.html')


@bp.route('/')
@bp.route('/create/<project_name>')
def create(project_name):
    if not current_user.is_anonymous:
        user = current_user.username
    else:
        user = 'anonymous'
    config = ProjectConfig(user, project_name)
    builder = BuildProject(config)
    builder.task_add(BuildDirsTask(config))
    builder.task_add(BuildConfigsTask(config))
    builder.task_add(CreateBlueprintsTask(config))
    builder.task_add(CreateAppInitTask(config))
    builder.task_add(CreateQuickStartScriptTask(config))
    builder.run_pipeline()
    return config.to_json()


@bp.route('/')
@bp.route('/zip/<project_name>')
def zip(project_name):
    if not current_user.is_anonymous:
        user = current_user.username
    else:
        user = 'anonymous'
    config = ProjectConfig(user, project_name)
    builder = BuildProject(config)
    builder.task_add(CreateArchiveTask(config))
    builder.run_pipeline()

    zip = project_name + '.zip'
    return redirect(url_for('static', filename=zip))


@bp.route('/')
@bp.route('/delete/<project_name>')
def delete(project_name):
    if not current_user.is_anonymous:
        user = current_user.username
    else:
        user = 'anonymous'
    config = ProjectConfig(user, project_name)
    builder = BuildProject(config)
    builder.task_add(DeleteProjectTask(config))
    builder.run_pipeline()

    return "deleted"