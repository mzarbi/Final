import json
import unittest

import requests
import time


class TestAPI(unittest.TestCase):

    def test_empty_url_set(self):
        url = "http://localhost:5000/v1/images/upload"
        payload = {"urls": []}
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload)).content
        self.assertTrue(json.loads(r)["jobId"] == None)

    def test_one_url(self):
        url = "http://localhost:5000/v1/images/upload"
        payload = {"urls": [
            "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg"
            ]
        }
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload)).content
        self.assertTrue(json.loads(r)["jobId"] != None)

    def test_multiple_urls(self):
        url = "http://localhost:5000/v1/images/upload"
        payload = {"urls": [
            "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg",
            "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d.jpg",
            "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_2d.jpg"
            ]
        }
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload)).content
        self.assertTrue(json.loads(r)["jobId"] != None)
        return json.loads(r)["jobId"]

    def test_check_job_status_short_timeout(self):
        jobId = self.test_multiple_urls()
        url = "http://localhost:5000/v1/images/upload/" + jobId
        payload = {}
        TIMEOUT = 1
        time.sleep(TIMEOUT)
        r = requests.get(url,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(payload)).content
        self.assertTrue(len(json.loads(r)["uploaded"]["pending"]) != 0)

    def test_check_job_status_long_timeout(self):
        jobId = self.test_multiple_urls()
        TIMEOUT = 15
        time.sleep(TIMEOUT)
        url = "http://localhost:5000/v1/images/upload/" + jobId
        payload = {}
        r = requests.get(url,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(payload)).content
        self.assertTrue(len(json.loads(r)["uploaded"]["pending"]) == 0)

    def test_request_uploaded_images(self):
        url = "http://localhost:5000/v1/images"
        payload = {}
        r = requests.get(url,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(payload)).content
        self.assertTrue(len(json.loads(r)["uploaded"]) != 0)


if __name__ == '__main__':
    unittest.main()