import requests


def test_add_result():
    url = "http://0.0.0.0:80/results"
    data = {
        "date": "2025-01-01",
        "result": "01 02 03 04 05 06 10"
    }
    res = requests.post(url=url, json=data)
    print(res.json())
    return res


def test_add_result_already_exists():
    test_add_result()
    res = test_add_result()
    print(res.json())


def test_get_result(type: str = '645'):
    url = "http://0.0.0.0:80/results/vietlott{0}".format(type)
    res = requests.get(url=url)
    print(res.json())


def test_get_result_by_date():
    url = "http://0.0.0.0:80/results/645/2025-01-01"
    res = requests.get(url=url)
    print(res.json())


def test_delete_result(date: str):
    url = "http://0.0.0.0:80/results/{0}".format(date)
    res = requests.delete(url=url)
    print(res.json())


if __name__ == "__main__":
    # test_get_result("655")
    # test_add_result()
    # test_get_result_by_date()
    # test_delete_result("3038")
    # test_add_result_already_exists()
    pass
