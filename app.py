from flask import Flask, render_template, redirect, url_for
from app import create_app
from app.routes.doctors import doctor_routes
from app.routes.patients import patient_routes
from app.routes.receptionist import receptionist_routes

app = create_app() 

@app.route('/')
def main_menu():
    return render_template('main_menu.html')  # might add a UI later


@app.route('/receptionist_portal')
def receptionist_portal():
    return redirect(url_for('receptionist_routes.receptionist_dashboard'))

@app.route('/doctor_portal')
def doctor_portal():
    return redirect(url_for('doctor_routes.doctor_dashboard'))


@app.route('/patient_portal')
def patient_portal():
    return redirect(url_for('patient_routes.patient_dashboard'))


@app.route('/exit')
def exit_app():
    return "Exiting the portal... Thank you for using the system!"

if __name__ == "__main__":
    app.run(debug=True)
