"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, session
from flask_babel import refresh
from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import ExampleForm, ContactForm
from models import ExampleModel

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/afcp/')
def afcp():
    return redirect(url_for("home"))


@app.route('/setlocale/<locale>')
def setlocale(locale):
    session['locale'] = locale
    refresh()
    return redirect(request.referrer)


@app.route('/about')
def about():
    return redirect(url_for("us"))


@app.route('/about/us')
def us():
    return render_template("about/nous.html")


@app.route('/about/paristech')
def paristech():
    return render_template("about/paristech.html")

@app.route('/about/paristechchine')
def paristechchine():
    return render_template("about/paristechchine.html")

@app.route('/about/activities')
def activities():
    return render_template("about/activities.html")

@app.route('/about/bureau')
def bureau():
    return render_template("about/bureau.html")

@app.route("/about/candidates")
def candidates():
    return render_template("about/candidature.html")

@app.route("/news")
def news():
    return redirect(url_for("huawei"))

@app.route("/news/huawei")
def huawei():
    return render_template("news/huawei.html")

@app.route("/amusement")
def amusement():
    return redirect(url_for("bal"))

@app.route("/amusement/bal")
def bal():
    return render_template("amusement/bal.html")

@app.route("/amusement/gala")
def gala():
    return render_template("amusement/gala.html")

@app.route("/research")
def research():
    return redirect(url_for('presentation'))

@app.route("/research/presentation")
def presentation():
    return render_template("research/presentation.html")

@app.route("/research/training")
def training():
    return render_template("research/training.html")

@app.route("/research/workpermit")
def workpermit():
    return render_template("research/workpermit.html")

@app.route("/research/alumni")
def alumni_research():
    return render_template("research/alumni.html")

@app.route("/research/newsletter")
def newsletter():
    return render_template("research/newsletter.html")

@app.route("/afcpchine")
def afcpchine():
    return redirect(url_for("alumnisalon"))

@app.route("/afcpchine/alumnisalon")
def alumnisalon():
    return render_template('afcpchine/alumnisalon.html')

@app.route("/misc")
def misc():
    return redirect(url_for('nuitdechine'))

@app.route("/misc/nuitdechine")
def nuitdechine():
    return render_template('misc/nuitdechine.html')

@app.route("/misc/itineraire-x")
def itineraire_x():
    return render_template('misc/itineraire-x.html')

@app.route('/misc/seminaire')
def seminaire():
    return render_template('misc/seminaire.html')


@app.route('/misc/roundtable')
def roundtable():
    return render_template('misc/roundtable.html')

@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        message = form.message.data

        sender = app.config['SENDER']
        to = app.config['CONTACT']
        subject = 'Message from {0}'.format(email)
        body = u"""
        Following is the message from {0}:

    {1}
    """.format(email, message)

        mail.send_mail(sender, to, subject, body, reply_to=email)

        flash('mail sent')
    return render_template('contact.html', form=form)

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
