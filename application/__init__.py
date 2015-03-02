"""
Initialize Flask app

"""
from flask import Flask, request
import os
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from werkzeug.debug import DebuggedApplication

app = Flask('application')
#os.environ["FLASK_CONF"] = 'DEV'

if os.getenv('FLASK_CONF') == 'DEV':
    # Development settings
    app.config.from_object('application.settings.Development')
    # Flask-DebugToolbar
    toolbar = DebugToolbarExtension(app)

    # Google app engine mini profiler
    # https://github.com/kamens/gae_mini_profiler
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    from gae_mini_profiler import profiler, templatetags

    @app.context_processor
    def inject_profiler():
        return dict(profiler_includes=templatetags.profiler_includes())
    app.wsgi_app = profiler.ProfilerWSGIMiddleware(app.wsgi_app)

elif os.getenv('FLASK_CONF') == 'TEST':
    app.config.from_object('application.settings.Testing')

else:
    app.config.from_object('application.settings.Production')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.globals['LOCALES'] = sorted(app.config['LANGUAGES'].keys())

from flask_admin.model import BaseModelView
from models import ActivityModel
from google.appengine.ext import ndb
from forms import ActivityForm

class NdbModel(BaseModelView):
    can_create = True
    can_edit = True
    can_delete = True

    def get_pk_value(self, model):
        return model.key.urlsafe()

    def scaffold_list_columns(self):
        return self.model._properties

    def scaffold_sortable_columns(self):
        return None

    def scaffold_form(self):
        return ActivityForm

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True):
        return 1, self.model.query()

    def get_one(self, urlsafe):
        key = ndb.Key(urlsafe=urlsafe)
        return key.get()

    def edit_form(self, obj=None):
        form = super(NdbModel, self).edit_form(obj)
        if request.method == 'GET':
            form.fr.title.data = obj.meta['fr']['title']
            form.fr.content.data = obj.meta['fr']['content']
            form.zh.title.data = obj.meta['zh']['title']
            form.zh.content.data = obj.meta['zh']['content']
        return form

    def create_model(self, form):
        name = form.name.data
        meta = {
            "fr": form.fr.data,
            "zh": form.zh.data
        }
        activity = ActivityModel(name=name, meta=meta)
        activity.put()
        return True

    def update_model(self, form, model):
        name = form.name.data
        meta = {
            "fr": form.fr.data,
            "zh": form.zh.data
        }
        model.name = name
        model.meta = meta
        model.put()
        return True

    def delete_model(self, model):
        model.key.delete()
        return True

admin = Admin(app)
admin.add_view(NdbModel(ActivityModel))
# Pull in URL dispatch routes
import urls
