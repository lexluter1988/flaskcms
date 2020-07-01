from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    name = StringField(_l('Project Name'), validators=[DataRequired()])
    packages = StringField(_l('Packages'), default='main, auth', validators=[DataRequired()])
    submit = SubmitField(_l('Sign In'))


class FeedBackForm(FlaskForm):
    name = StringField(_l('Your Name'), validators=[DataRequired()])
    email = StringField(_l('Your Email'), validators=[DataRequired()])
    content = TextAreaField(_l('Write what do you think'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
