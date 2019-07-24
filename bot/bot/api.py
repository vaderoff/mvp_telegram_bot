import requests

BASE_URL = 'http://web:8080/api/'


def send_sms_code(user_id):
    url = BASE_URL + 'sendSmsCode'
    resp = requests.get(url, params={'user_id': user_id}).json()
    return resp


def accept_sms_code(user_id, code):
    url = BASE_URL + 'acceptSmsCode'
    resp = requests.get(url, params={'user_id': user_id, 'code': code}).json()
    return resp['ok']


class BaseApiObject():
    def __init__(self, data, _allow_update=True):
        object.__setattr__(self, 'data', data)
        object.__setattr__(self, '_allow_update', _allow_update)

    def __getattr__(self, name):
        return self.data.get(name)

    def __setattr__(self, name, value):
        self.data[name] = value
        if self._allow_update:
            self.update()

    def update(self):
        pass


class User(BaseApiObject):
    URL = BASE_URL + 'users/'

    def update(self):
        url = self.URL + str(self.telegram_id) + '/'
        resp = requests.put(url, json=self.data)

    @classmethod
    def find(cls, telegram_id):
        url = cls.URL + str(telegram_id) + '/'
        resp = requests.get(url)
        if resp.status_code == requests.codes.ok:
            return cls(resp.json())

    @classmethod
    def create(cls, telegram_id, name):
        resp = requests.post(
            cls.URL, data={'telegram_id': telegram_id, 'name': name})
        if resp.status_code == 201:
            return cls(resp.json())


class Dialogue(BaseApiObject):
    URL = BASE_URL + 'dialogues/'

    def update(self):
        url = self.URL + str(self.telegram_id) + '/'
        resp = requests.put(url, json=self.data)

    def new_message(self, message, from_user=True):
        message = DialogueMessage.create(self.id, message, from_user)
        self.messages.append(message.id)

    @classmethod
    def find(cls, telegram_id):
        url = cls.URL + str(telegram_id) + '/'
        resp = requests.get(url)
        if resp.status_code == requests.codes.ok:
            return cls(resp.json())

    @classmethod
    def create(cls, telegram_id):
        resp = requests.post(
            cls.URL, data={'user': telegram_id})
        if resp.status_code == 201:
            return cls(resp.json())


class DialogueMessage(BaseApiObject):
    URL = BASE_URL + 'messages/'

    def update(self):
        url = self.URL + str(self.id) + '/'
        resp = requests.put(url, json=self.data)

    @classmethod
    def find(cls, id):
        url = cls.URL + str(self.id) + '/'
        resp = requests.get(url)
        if resp.status_code == requests.codes.ok:
            return cls(resp.json())

    @classmethod
    def create(cls, dialogue, message, from_user=True):
        resp = requests.post(cls.URL, data={
                             'dialogue': dialogue, 'message': message, 'from_user': from_user})
        if resp.status_code == 201:
            return cls(resp.json())
