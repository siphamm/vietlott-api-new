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
        cur.execute("INSERT INTO results (drawing_date, lottery_type, drawing_result) VALUES (%s, %s, %s)", [
                    add_result_input.date, add_result_input.lottery_type, add_result_input.result])
        db.commit()
    except RuntimeError as e:
        print(e)
        success = False
    finally:
        cur.close()
        db.close()

    return add_result_input if success else None
