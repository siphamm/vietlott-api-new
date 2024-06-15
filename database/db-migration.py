import os
import csv
from postgresql import open as postgres_open
from dotenv import load_dotenv

load_dotenv()


def insert_data_to_db(csv_file_path, db_url):
    # 1. Read the CSV file
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]

    # 2. Connect to PostgreSQL database
    db = postgres_open(db_url)

    try:
        insert_result = db.prepare(
            "INSERT INTO results(drawing_date, lottery_type, drawing_result) VALUES ($1, $2, $3)")
        rows_data = []
        for idx, row in enumerate(data):
            rows_data.append((row["date"], row["lotteryType"], row["result"]))

        insert_result.load_rows(rows_data)
    finally:
        db.close()


def display_top_100_records(db_url):
    # Connect to PostgreSQL database
    db = postgres_open(db_url)

    try:
        # Query the top 100 records
        result = db.query(
            "SELECT drawing_date, lottery_type, drawing_result FROM results LIMIT 100;")

        # Display the records
        for row in result:
            print("Drawing Date:", row["drawing_date"])
            print("Lottery Type:", row["lottery_type"])
            print("Drawing Result:", row["drawing_result"])
            print("------")

    finally:
        db.close()


def main():
    db_url = os.environ["POSTGRES_DB_CONNECTION_URL"]
    csv_file_path = "./data/vietlott-results.csv"
    insert_data_to_db(csv_file_path, db_url)
    display_top_100_records(db_url)


if __name__ == "__main__":
    main()
