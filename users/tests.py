import requests

from django.test     import TestCase, Client
from unittest.mock   import MagicMock, patch

from users.models    import User
class SignInKakaoTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id = "1234772",
            nickname = "김재엽",
            email    = "kjy120924@gmail.com",
            gender   = 1
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_signin_kakao_view_post_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                data = {
                    "id":1234772,
                    "properties":{
                        "nickname":"김재엽"
                    },
                    "kakao_account":{
                        "email":"kjy120924@gmail.com",
                        "gender":"male",
                    },
                }
                return data

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization":"fake access token"}
        response            = client.post("/users/signin-kakao", **headers)

        self.assertEqual(response.status_code, 200)

    @patch("users.views.requests")
    def test_signin_kakao_view_post_update(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                data = {
                    "id":1234772,
                    "properties":{
                        "nickname":"변경된김재엽"
                    },
                    "kakao_account":{
                        "email":"kjy120924@gmail.com",
                        "gender":"male",
                    },
                }
                return data

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization":"fake access token"}
        response            = client.post("/users/signin-kakao", **headers)

        self.assertEqual(response.status_code, 200)

    @patch("users.views.requests")
    def test_signin_kakao_view_post_create(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                data = {
                    "id":12347,
                    "properties":{
                        "nickname":"테스트"
                    },
                    "kakao_account":{
                        "email":"kimjy.par@gmail.com",
                        "gender":"male",
                    },
                }
                return data

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization":"fake access token"}
        response            = client.post("/users/signin-kakao", **headers)

        self.assertEqual(response.status_code, 201)

    @patch("users.views.requests")
    def test_signin_kakao_view_post_no_token(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                data = {
                    "id":12347,
                    "properties":{
                        "nickname":"테스트"
                    },
                    "kakao_account":{
                        "email":"kimjy.par@gmail.com",
                        "gender":"male",
                    },
                }
                return data

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_NoAuthorization":"fake access token"}
        response            = client.post("/users/signin-kakao", **headers)

        self.assertEqual(response.status_code, 401)

    @patch("users.views.requests")
    def test_signin_kakao_view_post_invalid_token(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                data = {
                    "error":12347,
                }
                return data

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization":"fake access token"}
        response            = client.post("/users/signin-kakao", **headers)

        self.assertEqual(response.status_code, 403)
