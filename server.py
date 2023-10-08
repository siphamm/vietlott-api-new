import csv
import os
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from postgresql import open as postgres_open
from dotenv import load_dotenv

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
    db_url = os.environ["POSTGRES_DB_CONNECTION_URL"]
    db = postgres_open(db_url)
    return db


def get_data(lottery_type: str = "645"):
    results = []
    try:
        db = get_db_connection()
        results = db.query(
            f"SELECT drawing_date, lottery_type, drawing_result FROM results where lottery_type='{lottery_type}' ORDER BY drawing_date DESC;")

        print(results)

    finally:
        db.close()

    return results

# @app.get("/results/{lottery_type}")
# def get_results(lottery_type: str):
#     drawings = get_data(lottery_type)
#     return {"type": lottery_type,
#             "results": drawings}


@app.get("/results/{lottery_type}")
def get_results(lottery_type: str):
    lottery_type_to_name = {
        "vietlott645": "645",
        "vietlott655": "655"
    }
    drawings = get_data(lottery_type_to_name[lottery_type])

    return [
        {
            "drawingId": idx + 1,
            "drawingDate": d["drawing_date"],
            "drawingResult": d["drawing_result"]
        } for idx, d in enumerate(drawings)
    ]


@app.post("/results/")
def add_result(add_result_input: AddResultInput):
    success = True
    try:
        db = get_db_connection()
        insert_result = db.prepare(
            "INSERT INTO results(drawing_date, lottery_type, drawing_result) VALUES ($1, $2, $3)")

        insert_result(
            add_result_input.date, add_result_input.lottery_type, add_result_input.result)
    except RuntimeError as e:
        print(e)
        success = False
    finally:
        db.close()

    return add_result_input if success else None
