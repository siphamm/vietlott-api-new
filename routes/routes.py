from fastapi import APIRouter
from database.database import get_db_connection
from models.models import AddResultInput
from utils.utils import normalize_drawing_result, get_drawing_results, validate_input

router = APIRouter()


@router.get("/results/{lottery_type}")
def get_results(lottery_type: str):
    # We're doing it here because the front-end is still using this format
    # Other APIs should use only 645 or 655
    lottery_type_to_name = {
        "vietlott645": "645",
        "vietlott655": "655"
    }
    drawings = get_drawing_results(lottery_type_to_name[lottery_type])

    return [
        {
            "drawingId": id,
            "drawingDate": drawing_date,
            "drawingResult": drawing_result
        } for idx, [id, drawing_date, drawing_result] in enumerate(drawings)
    ]


@router.get("/stats/{lottery_type}")
def get_stats(lottery_type: str = "645"):
    pass


@router.post("/results/")
def add_result(add_result_input: AddResultInput):
    success = True
    db = get_db_connection()
    cur = db.cursor()

    try:
        validate_input(add_result_input)
        normalized_drawing_result = normalize_drawing_result(
            add_result_input.result)

        cur.execute("INSERT INTO results (drawing_date, lottery_type, drawing_result) VALUES (%s, %s, %s)", [
                    add_result_input.date, add_result_input.lottery_type, normalized_drawing_result])
        db.commit()
    except RuntimeError as e:
        print(e)
        success = False
    finally:
        cur.close()
        db.close()

    return {
        "drawing_result": normalized_drawing_result,
        "success": success,
        "date": add_result_input.date,
        "lottery_type": add_result_input.lottery_type
    } if success else None

# Add a new endpoint to query all results given a drawing date and lottery type


@router.get("/results/{lottery_type}/{drawing_date}")
def get_result_by_date(lottery_type: str, drawing_date: str):
    results = []
    db = get_db_connection()
    cur = db.cursor()

    try:
        cur.execute(
            "SELECT id, drawing_date, drawing_result FROM results WHERE drawing_date = %s AND lottery_type = %s;", [drawing_date, lottery_type])

        results = cur.fetchall()

    finally:
        cur.close()
        db.close()

    return [
        {
            "drawingId": drawing_id,
            "drawingDate": drawing_date,
            "drawingResult": drawing_result
        } for idx, [drawing_id, drawing_date, drawing_result] in enumerate(results)
    ]


@router.delete("/results/{drawing_id}")
def delete_result(drawing_id: int):
    success = True
    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM results WHERE id = %s", [drawing_id])
        db.commit()
    except Exception as e:
        print(e)
        success = False
    finally:
        cur.close()
        db.close()
    return {"success": success}
