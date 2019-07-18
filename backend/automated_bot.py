import json
import random

import requests


class UserActivity:
    URL = 'http://127.0.0.1:8000/'

    def __init__(self, count_users):
        self.count_users = count_users
        self.user_ids = []

    def process(self):
        for number in range(self.count_users):
            self.register(number)

        header = self.login()
        return header, self.user_ids

    def register(self, number):
        body = {
            "city": "Kherson",
            "phone": "0991233113",
            "country": "Ukraine",
            "email": "test@test.com" + str(number),
            "username": "test_user" + str(number),
            "password": "123qwe1231" + str(number)
        }
        r = requests.post(self.URL + 'registration/', body)

        assert r.status_code == 201

        self.user_ids.append(json.loads(r.content)['id'])

    def login(self):
        body = {
            'username': 'test_user0',
            'password': '123qwe12310'
        }
        r = requests.post(self.URL + 'auth-jwt/', body)

        assert r.status_code == 200

        token = 'Bearer ' + json.loads(r.content)['token']
        return token


class PostEndpoint:
    URL = 'http://127.0.0.1:8000/post-endpoint/'

    def __init__(self, headers, user_ids, max_posts, max_likes):
        self.max_likes = max_likes
        self.max_posts = max_posts
        self.user_ids = user_ids
        self.headers = {'Authorization': headers}
        self.post_ids = []

    def process(self):
        for user_id in self.user_ids:
            self.create(user_id)

        self.put()
        self.delete()

    def create(self, user_id):
        posts = random.randint(1, self.max_posts)
        for i in range(posts):
            body = {
                'creator': user_id,
                'text': 'Test text for creating new post ' + str(user_id),
                'user_likes': []
            }
            r = requests.post(self.URL, body, headers=self.headers)

            assert r.status_code == 201

            self.post_ids.append(json.loads(r.content)['id'])

    def put(self):
        likes = random.randint(1, self.max_likes)
        for i in range(likes):
            url = self.URL + str(random.choice(self.post_ids)) + '/'
            body = {
                'user_id': random.choice(self.user_ids),
            }
            r = requests.put(url, body, headers=self.headers)

            assert r.status_code == 200

    def delete(self):
        body = {
            'user_id': 1,
        }
        r = requests.delete(self.URL + '1/', data=body, headers=self.headers)

        assert r.status_code == 200


def get_config():
    with open('config_bot.json', 'r') as file_json:
        data_file = json.load(file_json)
        return data_file['number_of_users'], data_file['max_posts_per_user'], data_file['max_likes_per_user']


if __name__ == '__main__':
    number_of_users, max_post, max_like = get_config()
    header, ids = UserActivity(number_of_users).process()
    PostEndpoint(header, ids, max_post, max_like).process()
