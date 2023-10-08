import requests


def test_add_result():
    url = "http://0.0.0.0:80/results"
    data = {
        "lottery_type": "645",
        "date": "2025-01-01",
        "result": "01 02 03 04 05 06"
    }
    res = requests.post(url=url, json=data)
    print(res.json())


def test_get_result():
    url = "http://0.0.0.0:80/results/vietlott645"
    res = requests.get(url=url)
    print(res.json())


if __name__ == "__main__":
    # test_get_result()
    test_add_result()
