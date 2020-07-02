import os

from flask import url_for, redirect, render_template, flash
from flask_babel import _
from flask_login import current_user

from app import db
from app.builders.builders import ProjectConfig, BuildProject
from app.builders.tasks import BuildDirsTask, CreateArchiveTask, BuildConfigsTask, DeleteProjectTask, \
    CreateBlueprintsTask, CreateAppInitTask, CreateQuickStartScriptTask
from app.main import bp
from app.main.forms import ProjectForm, FeedBackForm
from app.models import Project, FeedBack


def _get_username():
    if not current_user.is_anonymous:
        user = current_user.username
    else:
        user = 'anonymous'
    return user


def _build_project(project_name, packages=None) -> ProjectConfig:
    config = ProjectConfig(_get_username(), project_name, packages=packages)
    builder = BuildProject(config)
    builder.task_add(BuildDirsTask(config))
    builder.task_add(BuildConfigsTask(config))
    builder.task_add(CreateBlueprintsTask(config))
    builder.task_add(CreateAppInitTask(config))
    builder.task_add(CreateQuickStartScriptTask(config))
    builder.run_pipeline()
    return config


def _zip_project(project_name, packages=None):
    config = ProjectConfig(_get_username(), project_name, packages=packages)
    builder = BuildProject(config)
    builder.task_add(CreateArchiveTask(config))
    builder.run_pipeline()

    zip = project_name + '.zip'
    return url_for('static', filename=zip)


def _delete_project(project_name):
    config = ProjectConfig(_get_username(), project_name)
    builder = BuildProject(config)
    builder.task_add(DeleteProjectTask(config))
    builder.run_pipeline()


@bp.before_app_request
def before_request():
    if os.path.exists('app/maintenance'):
        return render_template('main/maintenance.html')


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/home.html')


@bp.route('/project', methods=['GET', 'POST'])
def project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        config = _build_project(form.name.data, form.packages.data)
        file_link = _zip_project(form.name.data, form.packages.data)
        flash(_('Congratulations, project has been created'))
        if current_user.is_anonymous:
            return render_template('main/projects_anon.html', title='New Project', form=form, url=file_link)
        else:
            project = Project(author=current_user,
                              name=config.project_name,
                              user_home=config.user_home,
                              project_home=config.project_home,
                              app_home=config.app_home,
                              packages=' '.join(config.packages),
                              archive=file_link)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('main.projects'))
    return render_template('main/project_new.html', title='New Project', form=form)


@bp.route('/project/delete/<project_id>', methods=['GET'])
def project_delete(project_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    if project:
        _delete_project(project.name)
        db.session.delete(project)
        db.session.commit()
        flash(_('Project deleted'))
    return redirect(url_for('main.projects'))


@bp.route('/projects', methods=['GET'])
def projects():
    projects = db.session.query(Project).\
        filter(Project.user_id == current_user.id).order_by(Project.timestamp.desc()).all()
    return render_template('main/projects.html', title='My Projects', projects=projects)


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedBackForm()
    if form.validate_on_submit():
        flash(_('Congratulations, we took your opinion. Thank you :)'))
        feedback = FeedBack(name=form.name.data, email=form.email.data, content=form.content.data)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/feedback.html', title='Feedback', form=form)


@bp.route('/feedbacks', methods=['GET'])
def feedbacks():
    feedbacks = db.session.query(FeedBack).all()
    return render_template('main/feedbacks.html', title='Feedbacks', feedbacks=feedbacks)


@bp.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html', title='About Project')


@bp.route('/projects/<project_id>', methods=['GET'])
def project_get(project_id):
    project = db.session.query(Project).\
        filter(Project.user_id == current_user.id).filter(Project.id == project_id).first()
    return render_template('main/project.html', title='Project', project=project)
