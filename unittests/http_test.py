import unittest
import requests
import json


class MyTestCase(unittest.TestCase):
    def test_sys_all(self):
        params = {}
        response = requests.get('http://localhost:7181/sys', data=json.dumps(params))
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_sys_cpu(self):
        params = {}
        response = requests.get('http://localhost:7181/sys/cpu', data=json.dumps(params))
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_sys_mem(self):
        params = {}
        response = requests.get('http://localhost:7181/sys/memory', data=json.dumps(params))
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_sys_storage(self):
        params = {}
        response = requests.get('http://localhost:7181/sys/storage', data=json.dumps(params))
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_sys_network(self):
        params = {}
        response = requests.get('http://localhost:7181/sys/network', data=json.dumps(params))
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_sys_services(self):
        params = {"services": ["google"]}
        response = requests.post('http://localhost:7181/sys/services', data=json.dumps(params))
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_sys_service(self):
        params = {"service": "google"}
        response = requests.post('http://localhost:7181/sys/service', data=json.dumps(params))
        print(response.text)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
