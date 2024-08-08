from db_connect import select_data_from_db


def validate_input(cnp: str, name: str):
    """Validate the input data for CNP and name."""
    if not cnp.isdigit():
        return "CNP must contain only digits."
    if len(cnp) != 13:
        return "CNP must be exactly 13 digits long."
    if not all(char.isalpha() or char in [' ', '-'] for char in name):
        return "Name should only contain letters, spaces, and hyphens."
    return None


def validate_doctor_credentials(config: dict, cnp: str, name: str, table: str = "medical_registry.personal_doctors"):
    """Check if the inserted CNP and name are in the database."""
    sql_query = f"SELECT * FROM {table} WHERE doctor_cnp = %s AND doctor_name = %s"
    provided_data = select_data_from_db(config, sql_query, (cnp, name))
    if not provided_data or len(provided_data) != 1:
        return None
    return provided_data[0]


def doctor_login(config: dict, cnp: str, name: str):

    """Create a function for the doctor to login with name and CNP"""

    print(f"Login attempts: CNP={cnp}, Name={name}")
    validation_error = validate_input(cnp, name)
    if validation_error:
        print(f"Validation error: {validation_error}")
        return validation_error
    doctor_data = validate_doctor_credentials(config, cnp, name)
    if not doctor_data:
        return "Invalid credentials."
    return doctor_data