import requests

url = "http://127.0.0.1:8000/results"
data = {
    "lottery_type": "645",
    "date": "2023-10-01",
    "result": "01 02 03 04 05 06"
}
res = requests.post(url=url, json=data)
print(res.json())
