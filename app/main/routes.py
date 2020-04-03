from flask import url_for, redirect, render_template, flash
from flask_login import current_user

from app import db
from app.builders.builders import ProjectConfig, BuildProject
from app.builders.tasks import BuildDirsTask, CreateArchiveTask, BuildConfigsTask, DeleteProjectTask, \
    CreateBlueprintsTask, CreateAppInitTask, CreateQuickStartScriptTask
from app.main import bp
from app.main.forms import ProjectForm


def _build_project(project_name, packages=None):
    if not current_user.is_anonymous:
        user = current_user.username
    else:
        user = 'anonymous'
    config = ProjectConfig(user, project_name, packages=packages)
    builder = BuildProject(config)
    builder.task_add(BuildDirsTask(config))
    builder.task_add(BuildConfigsTask(config))
    builder.task_add(CreateBlueprintsTask(config))
    builder.task_add(CreateAppInitTask(config))
    builder.task_add(CreateQuickStartScriptTask(config))
    builder.run_pipeline()
    return config.to_json()


def _zip_project(project_name, packages=None):
    if not current_user.is_anonymous:
        user = current_user.username
    else:
        user = 'anonymous'
    config = ProjectConfig(user, project_name, packages=packages)
    builder = BuildProject(config)
    builder.task_add(CreateArchiveTask(config))
    builder.run_pipeline()

    zip = project_name + '.zip'
    return url_for('static', filename=zip)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/base.html')


@bp.route('/')
@bp.route('/project', methods=['GET', 'POST'])
def project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        _build_project(form.name.data, form.packages.data)
        file_link = _zip_project(form.name.data, form.packages.data)
        flash('Congratulations, project has been created')
        if current_user.is_anonymous:
            return render_template('main/projects_anon.html', title='New Project', form=form, url=file_link)
        else:
            # TODO: here we save project in DB
            # db.session.add(user)
            # db.session.commit()
            return render_template('main/projects.html', title='New Project', form=form)
    return render_template('main/project_new.html', title='New Project', form=form)


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