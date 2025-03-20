from flask import Blueprint, request, jsonify
from app.models.database import db
from app.models.queries import *
import random
import webbrowser

patient_routes = Blueprint('patient_routes', __name__)

@patient_routes.route('/appointments/<int:patient_id>', methods=['GET'])
def patient_appointments(patient_id):
    """
    Fetch patient appointments or allow them to schedule a new one.
    """
    appointments = db.fetchall(GET_PATIENT_APPOINTMENTS, (patient_id,))
    headers = ['Appointment Id', 'Patient ID', 'Doctor ID', 'Appointment Date', 'Appointment Time', 'Reason for visit', 'Status']

    if appointments:
        return jsonify([dict(zip(headers, appointment)) for appointment in appointments])
    else:
        return jsonify({"message": "You do not have any scheduled appointments."}), 404


@patient_routes.route('/records/<int:patient_id>', methods=['GET'])
def access_records(patient_id):
    """
    Fetch patient medical records.
    """
    records = db.fetchall(GET_PATIENT_RECORDS, (patient_id,))
    headers = ['Record Id', 'Patient ID', 'Doctor ID', 'Diagnosis', 'Treatment', 'Prescription', 'Visit date', 'Doctors Notes']

    if records:
        return jsonify([dict(zip(headers, record)) for record in records])
    else:
        return jsonify({"message": "No medical records found. Please consult with your doctor."}), 404


@patient_routes.route('/prescription/<int:patient_id>', methods=['POST'])
def request_prescription(patient_id):
    """
    Allow a patient to request a prescription.
    """
    prescription = request.json.get('prescription')
    
    if not prescription:
        return jsonify({"error": "Prescription is required."}), 400

    db.execute("""
        INSERT INTO prescription_requests (patient_id, prescription, request_status)
        VALUES (%s, %s, %s)
    """, (patient_id, prescription, "Pending"))

    return jsonify({"message": f"Your request for '{prescription}' has been submitted and is pending approval."}), 201


@patient_routes.route('/pay_bills/<int:patient_id>', methods=['POST'])
def pay_bills(patient_id):
    """
    Patient makes a payment for their bills.
    """
    amount = request.json.get('amount')

    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount."}), 400

    payment_reference = f"PAY-{random.randint(100000, 999999)}"
    
    db.execute("""
        INSERT INTO payments (patient_id, amount, payment_status, paypal_transaction_id)
        VALUES (%s, %s, 'Pending', %s)
    """, (patient_id, amount, payment_reference))

    paypal_url = f"https://www.paypal.com/pay?hosted_button_id=nullamount={amount}&custom={payment_reference}"
    webbrowser.open(paypal_url)

    return jsonify({
        "message": f"Payment initiated. Your payment reference is: {payment_reference}. Please complete the payment."
    }), 201


@patient_routes.route('/feedback/<int:patient_id>', methods=['POST'])
def give_feedback(patient_id):
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
