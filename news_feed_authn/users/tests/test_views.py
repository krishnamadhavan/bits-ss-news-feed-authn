import pytest


class TestUserRegistration:
    path = "/api/auth/users/"
    data = {"username": "johndoe", "password": "user@123", "email": "johndoe@example.com"}
    content_type = "application/json"

    @pytest.mark.django_db
    def test_successful_user_registration(self, client):
        resp = client.post(path=self.path, data=self.data, content_type=self.content_type)
        assert resp.status_code == 201

    @pytest.mark.django_db
    def test_user_already_exists(self, client):
        resp = client.post(path=self.path, data=self.data, content_type=self.content_type)
        assert resp.status_code == 201

        resp = client.post(path=self.path, data=self.data, content_type=self.content_type)
        assert resp.status_code == 400


class TestUserLogin:
    path = "/api/auth/jwt/create/"
    content_type = "application/json"

    @pytest.mark.django_db
    def test_successful_user_login(self, client):
        path = "/api/auth/users/"
        data = {"username": "johndoe", "password": "user@123", "email": "johndoe@example.com"}
        resp = client.post(path=path, data=data, content_type=self.content_type)
        assert resp.status_code == 201

        data = {"username": "johndoe", "password": "user@123"}
        resp = client.post(path=self.path, data=data, content_type=self.content_type)
        assert resp.status_code == 200

    @pytest.mark.django_db
    def test_invalid_user_credentials(self, client):
        path = "/api/auth/users/"
        data = {"username": "johndoe", "password": "user@123", "email": "johndoe@example.com"}
        resp = client.post(path=path, data=data, content_type=self.content_type)
        assert resp.status_code == 201

        data = {"username": "johndoe", "password": "user@1234"}
        resp = client.post(path=self.path, data=data, content_type=self.content_type)
        assert resp.status_code == 401
