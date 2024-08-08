import db_connect as db
from datetime import datetime
import psycopg2 as ps

from doctor_auth import doctor_login, validate_input


def check_patient_exists(config, cnp, table: str = "medical_registry.patients"):
    """Check if a patient with the given CNP already exists in the database."""
    query = f"SELECT * FROM {table} WHERE patient_CNP = %s"
    existing_patient = db.select_data_from_db(config, query, (cnp,))
    return existing_patient


def add_new_patient(config, name, cnp, gender, doctor_id, table: str = "medical_registry.patients"):
    """Add a new patient to the database."""

    validation_error = validate_input(cnp, name)
    if validation_error:
        return validation_error

    # Check if the patient already exists
    existing_patient = check_patient_exists(config, cnp)
    if existing_patient:
        return "A patient with this CNP already exists."

    try:
        query = f"""INSERT INTO {table} (name, patient_CNP, gender, personal_doctor_id)
                    VALUES (%s, %s, %s, %s) RETURNING patient_id"""
        params = (name, cnp, gender, doctor_id)

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                patient_id = cursor.fetchone()[0]
                conn.commit()
                return patient_id
    except Exception as e:
        print(f"Error adding new patient: {e}")
        return None


def transfer_patient(config: dict, patient_cnp: str, patient_name: str, new_doctor_id: int,
                     table: str = "medical_registry.patients"):
    """Transfer a patient from another doctor to the current doctor"""

    # Validate the input firstly
    validation_error = validate_input(patient_cnp, patient_name)
    if validation_error:
        return validation_error

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Check if the patient exists and the name matches
                existing_patient = check_patient_exists(config, patient_cnp)
                if not existing_patient:
                    return "No patient found with this CNP."

                existing_patient_id = existing_patient[0]['patient_id']
                existing_patient_name = existing_patient[0]['name']

                if existing_patient_name.lower() != patient_name.lower():
                    return "The provided name does not match the CNP in our records."

                # Check if the patient is already assigned to the new doctor
                if existing_patient[0]['personal_doctor_id'] == new_doctor_id:
                    return "This patient is already assigned to you."

                # Update the doctor in the database
                update_query = f"""UPDATE {table} SET personal_doctor_id = %s 
                                   WHERE patient_id = %s RETURNING patient_id, name"""
                cursor.execute(update_query, (new_doctor_id, existing_patient_id))
                result = cursor.fetchone()
                conn.commit()

                if result:
                    return {"patient_id": result[0], "name": result[1]}
                else:
                    return "Failed to transfer patient."

    except ps.Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


def create_referral(config, patient_name, patient_cnp, specialization, clinic, current_doctor_id):
    """Create a referral ticket with specialization or clinic"""
    try:
        validation_error = validate_input(patient_cnp, patient_name)
        if validation_error:
            return validation_error

        # Check if the patient exists and belongs to the current doctor
        patient_query = """
        SELECT * FROM medical_registry.patients 
        WHERE patient_CNP = %s AND personal_doctor_id = %s
        """
        patient_data = db.select_data_from_db(config, patient_query, (patient_cnp, current_doctor_id))

        if not patient_data:
            return "No patient found with this CNP in your patient list."

        if patient_data[0]['name'].lower() != patient_name.lower():
            return "The provided name does not match the CNP in our records."

        # Check if the clinic exists
        clinic_query = "SELECT * FROM medical_registry.specialist_doctors WHERE LOWER(clinic) = LOWER(%s)"
        clinic_data = db.select_data_from_db(config, clinic_query, (clinic,))
        if not clinic_data:
            return f"The clinic '{clinic}' does not exist in our records."

        # Check if there's a specialist with the given specialization in the clinic
        specialist_query = """SELECT * FROM medical_registry.specialist_doctors 
        WHERE LOWER(specialization) = LOWER(%s) AND LOWER(clinic) = LOWER(%s)"""
        specialist_data = db.select_data_from_db(config, specialist_query, (specialization, clinic))

        if not specialist_data:
            return f" The specialization {specialization} was not found at {clinic} Clinic."

        specialist = specialist_data[0]['doctor_name']
        signed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        referral_details = f"""
        Referral Ticket
        Patient Name: {patient_name}
        Patient CNP: {patient_cnp}
        Referred to: Dr. {specialist}
        Specialization: {specialization.title()}
        Clinic: {clinic.capitalize()}
        Release Date: {signed_date}
        """

        with open(f"referral_{patient_name}.txt", "w") as file:
            file.write(referral_details)
        return True
    except Exception as e:
        print(f"Error creating referral: {e}")
        return f"An error occurred while creating the referral: {str(e)}"