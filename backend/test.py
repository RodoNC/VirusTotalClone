try:
    from server import app
    from json import dumps
    import unittest

except Exception as e:
    print(f"Some modules are missing {e}")


class FlaskTest(unittest.TestCase):

    # check for 200 status code on base route
    def test_index(self):
        print("Testing if the backend is running")
        tester = app.test_client(self)
        response = tester.get('/') # base roue
        status_code = response.status_code
        # print(response.data)
        # print("Testing API base route")
        self.assertEqual(200, status_code, msg='Test FAIlED!!!')





    # def test_hashRoute(self):
    #     print("Testing GET /hashes route")
    #     tester = app.test_client(self)
    #     response = tester.get('/hashes')  # Test GET on /hashes route
    #     status_code = response.status_code
    #     self.assertEqual(200, status_code, )


    def test_hashRoute_content(self):
        print("Testing POST response with valid hash")
        tester = app.test_client(self)
        hash_id = '11a30c3e7d930e6c6bb87f0baded5130'
        payload = {"Hash": hash_id}  # dummy data
        response = tester.post('/hashes', json=payload)  # Test POST on /hashes route
        status_code = response.status_code
        resp_json = response.json
        #print(resp_json)
        count = resp_json["count"]
        self.assertEqual(200, status_code, msg='Test FAILED!!! Error connecting to /hashes')
        self.assertEqual(count, 1)
        self.assertEqual(hash_id, resp_json["hash_report"][0]['Hash'], msg='Retrieved incorrect hash')
        self.assertEqual(1, len(resp_json['hash_report']), msg='The length of the hash report is not 1')

    def test_hashRoute_content_invalid_hash(self):
        print("Testing POST response with an invalid hash")
        tester = app.test_client(self)
        hash_id = 'invalid'
        payload = {"Hash": hash_id}  # dummy data
        response = tester.post('/hashes', json=payload)  # Test POST on /hashes route
        status_code = response.status_code
        resp_json = response.json
        self.assertEqual(200, status_code, msg="Test FAILED!!! Error connecting to the backend")
        self.assertEqual("INVALID Hash", resp_json['status_msg'], msg='Test FAILED!!! Did not handle invalid hash')

    def test_hash_popularity(self):
        print("Testing hash popularity")
        tester = app.test_client(self)
        hash_id = '11a30c3e7d930e6c6bb87f0baded5130'
        payload = {"Hash": hash_id}  # dummy data
        response = tester.post('/hashes', json=payload)  # Test POST on /hashes route
        status_code = response.status_code
        resp_json = response.json
        popularity = resp_json["hash_report"][0]["Popular"]

        # The backend should increment popularity by 1 after every hash lookup
        response_2 = tester.post('/hashes', json=payload)
        popularity_2 = response_2.json["hash_report"][0]["Popular"]
        self.assertEqual(200, status_code, msg="Test FAILED!!! Error connecting to /hashes")
        self.assertEqual(popularity + 1, popularity_2, msg='Test FAILED!!! Popularity did not increment')

    def test_hash_limit(self):
        print("Testing how backend responds to continuous requests")
        tester = app.test_client(self)
        hashes = ["137904b4aaf8501370638566a2d3428c",
            "5c3feeb786cde27adac18d852b7751f6",
            "b5f0b12f484c5c330d8fe457e8a0da71",
            "43ee94f386de8c27089d63b13989027d",
            "1a2589f4ab1bcdb49c841012c9bf2d36",
            "85aff436ea1995b2829f9b15eb5dd07a",
            "8973d1fac3ead720f28ad4e53c77c72c",
            "132895f3b844a9c0eb2be76adf7ca747",
            "e52aa07960eb748775c030139b34ed05",
            "71ae95bb32eecad513631c9ca209b1b8",
            "3c0556a9bbfcd64f5f4cd3e5a23bcdc7",
            "7ee6674ef6d21b3a8566b84c64f7ec62",
            "24f1274e3bb8eb3933bc645181e48539",
            "c66f6b1f0513e13578d86fb66e7009b3",
            "1a4766827a39a15e324d8adacd9c0448",
            "541bbc00d78516e3c1d199e51e56bc10",
            "289414cc59b144922be95d9f3b3653cf",
            "c5f05336a76f5b8833d4f5d38890f16e"]

        # print(len(hashes))

        for i in range(len(hashes)):
            payload = {"Hash": hashes[i]}  # dummy data
            response = tester.post('/hashes', json=payload)  # Test POST on /hashes route
            status_code = response.status_code
            resp_json = response.json
            count = resp_json["count"]

            self.assertEqual(200, status_code, msg='Test FAILED!!! Error connecting to /hashes')
            self.assertEqual(count, 1)
            self.assertEqual(hashes[i], resp_json["hash_report"][0]['Hash'], msg='Retrieved incorrect hash')
            self.assertEqual(1, len(resp_json['hash_report']), msg='The length of the hash report is 0')

            #print(i, resp_json)

    def test_extra_route(self):
        print("Testing /extra route")
        tester = app.test_client(self)
        response = tester.get('/extra')  # base roue
        status_code = response.status_code
        resp_json = response.get_json()
        self.assertEqual(200, status_code, msg='Test FAIlED!!!')
        self.assertEqual("application/json", response.headers["Content-Type"],   msg="Did not return json object")
        self.assertGreater(len(resp_json['db_report'][0]['Date']), 0, msg="FAIL!! Returned empty array")
        self.assertGreater(len(resp_json['db_report'][0]['Popular']), 0, msg="FAIL!! Returned empty array")






if __name__ == '__main__':
    unittest.main()
