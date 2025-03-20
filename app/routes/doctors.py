from flask import Blueprint, request, jsonify
from app.models.database import db
from app.models.queries import *
from receptionist import view_appointments

doctor_routes = Blueprint("doctors", __name__)

@doctor_routes.route("/records/<int:patient_id>", methods=["GET"])
def view_patient_records(patient_id):
    """Fetch patient medical records"""
    patient_records = db.fetch_all(GET_PATIENT_RECORDS, (patient_id,))

    if patient_records:
        headers = ['record_id', 'patient_id', 'doctor_id', 'diagnosis', 'treatment', 
                   'prescription', 'visit_date', 'notes']
        return jsonify({"patient_id": patient_id, "records": patient_records})
    return jsonify({"error": "No records found"}), 404


@doctor_routes.route("/medical_records/update", methods=["PUT"])
def update_medical_records():
    """Update medical records (diagnosis, treatment, prescription, notes)"""
    data = request.json
    patient_id = data.get("patient_id")
    field_name = data.get("field_name")
    new_value = data.get("new_value")

    if not all([patient_id, field_name, new_value]):
        return jsonify({"error": "Missing required fields"}), 400

    valid_fields = ["diagnosis", "treatment", "prescription", "doctor_note"]
    if field_name not in valid_fields:
        return jsonify({"error": f"Invalid field name. Choose from {valid_fields}"}), 400

    # Check if patient exists
    patient_name_tuple = db.fetch_one("SELECT first_name FROM patients WHERE patient_id = %s", (patient_id,))
    if not patient_name_tuple:
        return jsonify({"error": f"No patient found with ID {patient_id}"}), 404

    # Update record
    db.execute(f"UPDATE medical_records SET {field_name} = %s WHERE patient_id = %s", (new_value, patient_id))
    return jsonify({"message": f"{field_name.capitalize()} updated successfully"})


@doctor_routes.route("/prescriptions/<int:patient_id>", methods=["GET"])
def generate_prescriptions(patient_id):
    """Retrieve a patient's prescriptions"""
    prescriptions = db.fetch_all(GET_PATIENT_PRESCRIPTION, (patient_id,))

    if prescriptions:
        return jsonify({"patient_id": patient_id, "prescriptions": prescriptions})
    return jsonify({"error": "No prescriptions found"}), 404


@doctor_routes.route("/lab_reports/<int:patient_id>", methods=["GET"])
def view_lab_reports(patient_id):
    """Retrieve lab reports for a patient"""
    lab_reports = db.fetch_all(GET_NOTES, (patient_id,))

    if lab_reports:
        return jsonify({"patient_id": patient_id, "lab_reports": lab_reports})
    return jsonify({"error": "No lab reports found"}), 404


@doctor_routes.route("/notes", methods=["POST"])
def write_notes():
    """Write doctor notes for a patient"""
    data = request.json
    patient_id = data.get("patient_id")
    notes = data.get("notes")

    if not all([patient_id, notes]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if patient exists
    patient_name_tuple = db.fetch_one("SELECT first_name FROM patients WHERE patient_id = %s", (patient_id,))
    if not patient_name_tuple:
        return jsonify({"error": f"No patient found with ID {patient_id}"}), 404

    db.execute(UPDATE_DOCTOR_NOTE, (notes, patient_id))
    return jsonify({"message": "Doctor's notes added successfully"})


@doctor_routes.route("/prescription_requests/<int:patient_id>", methods=["GET", "PUT"])
def prescription_requests(patient_id):
    """Fetch or approve/deny prescription requests"""
    if request.method == "GET":
        requests = db.fetch_all(GET_PATIENT_REQUESTS, (patient_id,))
        if requests:
            return jsonify({"patient_id": patient_id, "requests": requests})
        return jsonify({"error": "No prescription requests found"}), 404

    elif request.method == "PUT":
        data = request.json
        request_status = data.get("request_status")

        if request_status not in ["Accepted", "Denied"]:
            return jsonify({"error": "Invalid request status, use 'Accepted' or 'Denied'"}), 400

        db.execute("""
            UPDATE prescription_requests 
            SET request_status = %s
            WHERE patient_id = %s
        """, (request_status, patient_id))

        return jsonify({"message": f"Prescription request {request_status}"})


@doctor_routes.route("/appointments", methods=["GET"])
def get_appointments():
    """Retrieve all patient appointments"""
    return view_appointments()
