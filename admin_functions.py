import db_connect as db
import psycopg2 as ps

from doctor_auth import validate_input


def add_personal_doctor(config: dict, name: str, cnp: str, table: str = "medical_registry.personal_doctors"):
    """Add a new personal doctor to the database after checking for duplicates.
    Returns doctor ID if added successfully, error message otherwise."""

    # Validate inputs
    validation_error = validate_input(cnp, name)
    if validation_error:
        return validation_error

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Check if the doctor already exists
                check_query = f"SELECT * FROM {table} WHERE doctor_cnp = %s"
                cursor.execute(check_query, (cnp,))
                existing_doctor = cursor.fetchone()

                if existing_doctor:
                    return "A doctor with this CNP already exists. Cannot add a duplicate."

                # Add new doctor to the database
                insert_query = f"INSERT INTO {table} (doctor_name, doctor_cnp) VALUES (%s, %s) RETURNING doctor_id"
                cursor.execute(insert_query, (name, cnp))
                new_doctor_id = cursor.fetchone()[0]
                conn.commit()
                return new_doctor_id

    except ps.Error as e:
        print(f"Database error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def remove_personal_doctor(config: dict, cnp: str, name: str, table: str = "medical_registry.personal_doctors"):
    """Remove a personal doctor from the database.
    Returns doctor ID if removed successfully, error message otherwise"""

    # Validate input
    validation_error = validate_input(cnp, name)
    if validation_error:
        return validation_error

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Check if the doctor exists with the given CNP and name
                check_query = f"SELECT * FROM {table} WHERE doctor_cnp = %s AND doctor_name = %s"
                cursor.execute(check_query, (cnp, name))
                existing_doctor = cursor.fetchone()

                if not existing_doctor:
                    return "No doctor found with this CNP and name. Cannot remove."

                # Remove the doctor from the database
                delete_query = f"DELETE FROM {table} WHERE doctor_cnp = %s AND doctor_name = %s RETURNING doctor_id"
                cursor.execute(delete_query, (cnp, name))
                removed_doctor_id = cursor.fetchone()[0]
                conn.commit()
                return removed_doctor_id

    except ps.Error as e:
        print(f"Database error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_all_doctors(config: dict, table: str = "medical_registry.personal_doctors") -> list:
    """Create function to see all personal doctors from database.
    Returns list of all doctors"""

    query = f"SELECT * FROM {table}"
    doctors = db.select_data_from_db(config, query)
    return doctors
