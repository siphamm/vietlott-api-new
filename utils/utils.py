from models.models import AddResultInput
from database.database import get_db_connection


def normalize_drawing_result(drawing_result: str):
    # Normalize the drawing result string by doing the following:
    # 1. Remove all spaces and non-digit characters
    # 2. Ensure there are 10 or 12 digits in the string
    # 3. Add a space after every 2 digits
    # 4. Return the normalized string
    drawing_result = "".join([c for c in drawing_result if c.isdigit()])
    drawing_result = " ".join([drawing_result[i:i + 2]
                               for i in range(0, len(drawing_result), 2)])

    return drawing_result


def validate_input(add_result_input: AddResultInput):
    if len(normalize_drawing_result(add_result_input.result)) != 17 and len(normalize_drawing_result(add_result_input.result)) != 20:
        raise RuntimeError("Invalid result length. Should be 17 or 20")

    if len(add_result_input.date) != 10:
        raise RuntimeError("Invalid date length")


def get_lottery_type(normalized_result_str: str):
    if len(normalized_result_str) == 17:
        return "645"

    if len(normalized_result_str) == 20:
        return "655"


def get_drawing_results(lottery_type: str = "645"):
    results = []
    db = get_db_connection()
    cur = db.cursor()

    try:
        cur.execute(
            "SELECT id, drawing_date, drawing_result FROM results where lottery_type=%s ORDER BY drawing_date DESC LIMIT 500;", [lottery_type])

        results = cur.fetchall()

    finally:
        cur.close()
        db.close()

    return results
