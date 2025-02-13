import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from backend.extensions import db
from backend.routes.auth_routes import auth_blueprint
from backend.routes.budget_routes import budgets_blueprint
from backend.routes.dashboard_routes import dashboard_blueprint
from backend.routes.transactions_routes import transactions_blueprint
from backend.routes.users_routes import users_blueprint

app = Flask(__name__,
            template_folder='/app/frontend/templates/',
            static_folder='/app/frontend/static/')  # prepend /app/ for Docker

CORS(app,
     resources={r"/api/*": {"origins": "http://localhost:3000"}},
     supports_credentials=True)


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
app.register_blueprint(budgets_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(transactions_blueprint)
app.register_blueprint(users_blueprint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
