from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    packages = StringField('Packages', default='main, auth', validators=[DataRequired()])
    submit = SubmitField('Sign In')