#coding=utf-8
"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from wtforms import Form
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import ExampleModel


class ClassicExampleForm(wtf.Form):
    example_name = wtf.TextField('Name', validators=[validators.Required()])
    example_description = wtf.TextAreaField('Description', validators=[validators.Required()])

# App Engine ndb model form example
ExampleForm = model_form(ExampleModel, wtf.Form, field_args={
    'example_name': dict(validators=[validators.Required()]),
    'example_description': dict(validators=[validators.Required()]),
})


class ContactForm(wtf.Form):
    email = wtf.StringField('Votre e-mail',
                            validators=[validators.Email()])
    message = wtf.TextAreaField(u"Le message à envoyer à l'AFCP :",
                                validators=[validators.InputRequired()])

class ActivityEntryForm(Form):
    title = wtf.StringField('title')
    content = wtf.TextAreaField('content')
    
class ActivityForm(Form):
    name = wtf.StringField('name', validators=[validators.InputRequired()])
    fr = wtf.FormField(ActivityEntryForm)
    zh = wtf.FormField(ActivityEntryForm)
