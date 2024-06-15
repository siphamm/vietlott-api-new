import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AddResultInput(BaseModel):
    lottery_type: str
    date: str
    result: str


def get_db_connection():
    conn = psycopg2.connect(database=os.environ["POSTGRES_DB_NAME"],
                            host=os.environ["POSTGRES_HOST"],
                            user=os.environ["POSTGRES_USER"],
                            password=os.environ["POSTGRES_PASSWORD"])
    return conn


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


@app.get("/results/{lottery_type}")
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
            "drawingId": idx + 1,
            "drawingDate": drawing_date,
            "drawingResult": drawing_result
        } for idx, [drawing_date, drawing_result] in enumerate(drawings)
    ]


@app.get("/stats/{lottery_type}")
def get_stats(lottery_type: str = "645"):
    pass


@app.post("/results/")
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


@app.get("/results/{lottery_type}/{drawing_date}")
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


@app.delete("/results/{drawing_id}")
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


def validate_input(add_result_input: AddResultInput):
    if add_result_input.lottery_type not in ["645", "655"]:
        raise RuntimeError("Invalid lottery type")

    if add_result_input.lottery_type == "645" and len(normalize_drawing_result(add_result_input.result)) != 17:
        raise RuntimeError("Invalid result length for 645")

    if add_result_input.lottery_type == "655" and len(normalize_drawing_result(add_result_input.result)) != 20:
        raise RuntimeError("Invalid result length for 655")

    if len(add_result_input.date) != 10:
        raise RuntimeError("Invalid date length")
