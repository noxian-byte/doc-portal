from flask import Flask
from app.models.database import db
from app.routes.doctors import doctor_routes
from app.routes.patients import patient_routes
from app.routes.receptionist import receptionist_routes

def create_app():
    app = Flask(__name__)

    
    app.register_blueprint(doctor_routes, url_prefix="/doctors")
    app.register_blueprint(patient_routes, url_prefix="/patients")
    app.register_blueprint(receptionist_routes, url_prefix="/receptionist")

    return app
