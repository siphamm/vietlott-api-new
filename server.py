import csv
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


def get_data(lottery_type: str = "645"):
    results = []
    with open('data/vietlott-results.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            [lDate, lType, lResult] = row
            if lType == lottery_type:
                results.append([lDate, lResult.split()])

    results.sort(key=lambda r: r[0], reverse=True)
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
            "drawingDate": d[0],
            "drawingResult": " ".join(d[1])
        } for idx, d in enumerate(drawings)
    ]


@app.post("/results/")
def add_result(add_result_input: AddResultInput):
    with open('data/vietlott-results.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(
            [add_result_input.date,
             add_result_input.lottery_type,
             add_result_input.result])

    return add_result_input
