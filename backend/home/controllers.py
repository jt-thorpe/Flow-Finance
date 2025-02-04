from flask import Blueprint, Response, redirect, render_template, url_for

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/', methods=['GET'])
def home_redirect() -> Response:
    """Redirect '/' to the '/home' page."""
    return redirect(url_for('home.home_serve'))


@home_blueprint.route('/home', methods=['GET'])
def home_serve() -> str:
    """Render the 'home.html' page."""
    return render_template('home.html')
