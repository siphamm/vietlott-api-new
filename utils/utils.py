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
    if add_result_input.lottery_type not in ["645", "655"]:
        raise RuntimeError("Invalid lottery type")

    if add_result_input.lottery_type == "645" and len(normalize_drawing_result(add_result_input.result)) != 17:
        raise RuntimeError("Invalid result length for 645")

    if add_result_input.lottery_type == "655" and len(normalize_drawing_result(add_result_input.result)) != 20:
        raise RuntimeError("Invalid result length for 655")

    if len(add_result_input.date) != 10:
        raise RuntimeError("Invalid date length")


def get_drawing_results(lottery_type: str = "645"):
    results = []
    db = get_db_connection()
    cur = db.cursor()

    try:
        cur.execute(
            "SELECT drawing_date, drawing_result FROM results where lottery_type=%s ORDER BY drawing_date DESC;", [lottery_type])

        results = cur.fetchall()

    finally:
        cur.close()
        db.close()

    return results
