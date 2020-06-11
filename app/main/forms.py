from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    packages = StringField('Packages', default='main, auth', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class FeedBackForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired()])
    content = TextAreaField('Write what do you think', validators=[DataRequired()])
    submit = SubmitField('Submit')
