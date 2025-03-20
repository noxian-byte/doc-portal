from flask import Blueprint, request, jsonify
from app.models.database import db
from app.models.queries import *
import random
import webbrowser

receptionist_routes = Blueprint('receptionist_routes', __name__)

@receptionist_routes.route('/appointments/<int:patient_id>', methods=['GET'])
def receptionist_appointments(patient_id):
    """
    Fetch appointments for a patient or allow a receptionist to schedule a new appointment.
    """
    appointments = db.fetchall(GET_PATIENT_APPOINTMENTS, (patient_id,))
    headers = ['Appointment Id', 'Patient ID', 'Doctor ID', 'Appointment Date', 'Appointment Time', 'Reason for visit', 'Status']

    if appointments:
        return jsonify([dict(zip(headers, appointment)) for appointment in appointments])
    else:
        return jsonify({"message": "No appointments found for this patient."}), 404


@receptionist_routes.route('/appointments', methods=['POST'])
def schedule_appointment():
    """
    Receptionist schedules a new appointment for a patient.
    """
    patient_id = request.json.get('patient_id')
    doctor_id = request.json.get('doctor_id')
    appointment_date = request.json.get('appointment_date')
    appointment_time = request.json.get('appointment_time')
    reason_for_visit = request.json.get('reason_for_visit')

    if not all([patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit]):
        return jsonify({"error": "All fields are required to schedule an appointment."}), 400

    db.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, status)
        VALUES (%s, %s, %s, %s, %s, 'Scheduled')
    """, (patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit))

    return jsonify({"message": "Appointment successfully scheduled."}), 201


@receptionist_routes.route('/records/<int:patient_id>', methods=['GET'])
def access_patient_records(patient_id):
    """
    Fetch medical records for a patient.
    """
    records = db.fetchall(GET_PATIENT_RECORDS, (patient_id,))
    headers = ['Record Id', 'Patient ID', 'Doctor ID', 'Diagnosis', 'Treatment', 'Prescription', 'Visit date', 'Doctors Notes']

    if records:
        return jsonify([dict(zip(headers, record)) for record in records])
    else:
        return jsonify({"message": "No medical records found. Please consult with your doctor."}), 404


@receptionist_routes.route('/prescription_request/<int:patient_id>', methods=['POST'])
def request_prescription(patient_id):
    """
    Allow a receptionist to request a prescription on behalf of a patient.
    """
    prescription = request.json.get('prescription')
    
    if not prescription:
        return jsonify({"error": "Prescription is required."}), 400

    db.execute("""
        INSERT INTO prescription_requests (patient_id, prescription, request_status)
        VALUES (%s, %s, %s)
    """, (patient_id, prescription, "Pending"))

    return jsonify({"message": f"Your request for '{prescription}' has been submitted and is pending approval."}), 201


@receptionist_routes.route('/pay_bills/<int:patient_id>', methods=['POST'])
def receptionist_pay_bills(patient_id):
    """
    Receptionist processes a payment for a patient's bills.
    """
    amount = request.json.get('amount')

    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount."}), 400

    payment_reference = f"PAY-{random.randint(100000, 999999)}"
    
    db.execute("""
        INSERT INTO payments (patient_id, amount, payment_status, paypal_transaction_id)
        VALUES (%s, %s, 'Pending', %s)
    """, (patient_id, amount, payment_reference))
    
    # invalid link
    paypal_url = f"https://www.paypal.com/pay?hosted_button_id=nullamount={amount}&custom={payment_reference}"
    webbrowser.open(paypal_url)

    return jsonify({
        "message": f"Payment initiated. Your payment reference is: {payment_reference}. Please complete the payment."
    }), 201


@receptionist_routes.route('/feedback/<int:patient_id>', methods=['POST'])
def receptionist_feedback(patient_id):
    """
    Allow patients to give feedback for their doctor or receptionist.
    """
    recipient = request.json.get('recipient')
    feedback_text = request.json.get('feedback_text')

    if recipient not in ["doctor", "receptionist"]:
        return jsonify({"error": "Recipient must be either 'doctor' or 'receptionist'."}), 400

    if not feedback_text:
        return jsonify({"error": "Feedback text cannot be empty."}), 400

    db.execute("""
        INSERT INTO feedback (patient_id, recipient, feedback_text)
        VALUES (%s, %s, %s)
    """, (patient_id, recipient, feedback_text))

    return jsonify({"message": "Thank you for your feedback!"}), 201
