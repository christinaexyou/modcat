from functools import wraps
from flask import Flask, render_template, Response, request, redirect, session
from flask_session import Session

from datetime import timedelta

from login.login_manager import LoginManager
from managers.project_manager import ProjectManager
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'b5e3170d338b6d8e5967b8e0'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.permanent_session_lifetime = timedelta(minutes=60)
Session(app)

# 'application' reference required for wgsi / gunicorn
# https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#using-images-python-configuration
#application = app
# run gunicorn manually
# gunicorn wsgi:application -b 0.0.0.0:8080
###################
# This is just for testing timeout.  Remove when not needed
@app.before_request
def before_request():
    user = session.get('user')
    if user is None:
        print("Session ended")



###################

def login_required(f):
    """
    This function is used to decorate all url endpoints.  If a user object is not present in the Session,
    redirect back to the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return render_template("loginPage.html", message="Session has expired.  Please log in")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def start():
    return render_template("loginPage.html")


@app.route('/loginValidation', methods=['POST'])
def loginValidation():
    username = request.form.get('username')
    password = request.form.get('password')
    login_msg, user = LoginManager.login_validation(username, password)

    if login_msg == 'ok':
        session['user'] = user  # Put user object into the Session at login time.
        return render_template('landingPage.html', logged_in_user=user)
    else:
        return render_template('loginPage.html', message=login_msg)

@app.route('/log_out')
def log_out():
    session.clear()
    return render_template('loginPage.html')

#NOTE: This route is never called.
@app.route('/landing_page')
@login_required
def landing_page():
    user = session['user']
    print("  Landing page    userid: {}  username: {}".format(user.userid, user.username))
    return render_template('landingPage.html')

@app.route("/projectPage", methods=['POST', 'GET'])
@login_required
def project_page():
    projid = request.args.get('projectid')
    project_manager = ProjectManager()
    project = project_manager.get_project_by_id(projid)
    #return render_template("projectPage.html", project_id=projid, teamid=project.teamid, modelid=project.modelid,
    #                       projectname=project.projectname)
    return render_template("projectPage.html", project_id=projid)


if __name__ == '__main__':
    app.run(debug=True, port=5050)


