from flask import Flask, render_template, Response, request, redirect
from login.login_manager import LoginManager
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
# 'application' reference required for wgsi / gunicorn
# https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#using-images-python-configuration
#application = app



# run gunicorn manually
# gunicorn wsgi:application -b 0.0.0.0:8080


@app.route('/')
def start():
    return render_template("loginPage.html")


@app.route('/loginValidation', methods=['POST'])
def loginValidation():
    username = request.form.get('username')
    password = request.form.get('password')
    login_msg = LoginManager.login_validation(username, password)
    if login_msg == 'ok':
        return render_template('landingPage.html')
    else:
        return render_template('loginPage.html', message = login_msg)

@app.route('/landing_page')
def landing_page():
    return render_template('landingPage.html')

if __name__ == '__main__':
    app.run(debug=True, port=5050)


