from flask import Flask
from src.routes import messaging_bp
from src.extensions import db, migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messaging.db"
# app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

# Register the messaging blueprint
app.register_blueprint(messaging_bp, url_prefix="/")
