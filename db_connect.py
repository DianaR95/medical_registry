import json
import psycopg2 as ps


def read_config(path: str = "config.json") -> dict:

    """Connect to the database"""

    try:
        config = {}
        with open(path, "r") as f:
            config = json.loads(f.read())
        return config
    except Exception as e:
        print(f"Error to read config {e}")
        return {}


def select_data_from_db(config: dict, sql_query: str, params: tuple = ()) -> list:

    """Returns a list of dictionaries representing the rows from the result set.
    If an error occurs, it returns an empty list.
    The list of dictionaries represents the query results.
    Each dictionary corresponds to a row, with keys as column names."""

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, params)
                items = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, item)) for item in items]
    except Exception as e:
        print(f"Error when selecting data {e}")
        return []

