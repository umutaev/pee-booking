import requests


class UserBackend:
    def __init__(self, server: str) -> None:
        self._server = server

    def check_user(self, username: str = None, user_id: int = None) -> bool:
        if user_id is not None:
            r = requests.get(self._server + "/" + username)
            if r.status_code == 400:
                return False
        if username is not None:
            r = requests.get(self._server + "/" + user_id)
            if r.status_code == 400:
                return False
        if user_id is None and username is None:
            raise ValueError("Specify username or userid")
        return True

    def create_user(
        self,
        username: str,
        user_id: int,
        floor: str,
        sex: str,
    ) -> bool:
        if self.check_user(username=username):
            return False
        r = requests.post(
            self._server + "/" + username,
            data=str(user_id).encode("utf-8"),
            headers={"Content-Type": "text/plain"},
        )
        if r.status_code == 400:
            return False
        r = requests.post()
        return True


class TimetableBackend:
    def __init__(self, server: str) -> None:
        self._server = server

    def sign_up(self, time) -> bool:
        ...  # TODO: check if time is available and make a request to sign up

    def cancel(self, username) -> bool:
        ...  # TODO: check if user is signed up and if so, cancel reservation

    def fetch(self) -> ...:
        ...  # TODO: fetch timetable and return it
