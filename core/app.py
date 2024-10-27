import os
from datetime import timedelta

from flask import Flask, render_template

from auth.controllers import auth_blueprint
from core.extensions import db
from transactions.controllers import transactions_blueprint

app = Flask(__name__,
            template_folder='/app/frontend/templates/',
            static_folder='/app/frontend/static/')  # prepend /app/ for Docker


# Flask app configuration
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']  # for session
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLOW_DB_URI']  # for PSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


# Initialise the database
db.init_app(app)
with app.app_context():
    db.create_all()


# Register Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(transactions_blueprint)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
