import requests
import unittest


class TestAddResult(unittest.TestCase):
    def test_invalid_input(self):
        url = "http://0.0.0.0:80/results"
        data = {
            "lottery_type": "645",
            "date": "2025-01-01",
            "result": "01 02 03 04 05 06 10 19"
        }
        res = requests.post(url=url, json=data)

        # Assert that the request failed (status code is not 200)
        self.assertNotEqual(res.status_code, 200)

        # Assert that the response does not contain the added result
        response_data = res.json()
        self.assertNotIn(data, response_data)


if __name__ == "__main__":
    unittest.main()
