import json
import random

import requests
from faker import Faker

CONFIG_FILE = "config.json"

BASE_URL = "http://localhost:8000/api/"

USER_SIGNUP_URL = BASE_URL + "user/signup/"
USER_TOKEN_OBTAIN_URL = BASE_URL + "user/token/"
USER_PROFILE_URL = BASE_URL + "user/profile/"

CREATE_POST_URL = BASE_URL + "posts/"
LIKE_POST_URL = BASE_URL + "posts/like/"


def read_config():
    with open(CONFIG_FILE) as config_file:
        bot_config = json.load(config_file)

    return (
        bot_config["number_of_users"],
        bot_config["max_posts_per_user"],
        bot_config["max_likes_per_user"],
    )


def get_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_user():
    fake = Faker()
    user_data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
    }
    response = requests.post(USER_SIGNUP_URL, data=user_data)

    if response.status_code == 201:
        username = user_data["username"]
        password = user_data["password"]

        token = login_user(user_data["username"], user_data["password"])

        return username, password, token


def login_user(username, password):
    login_data = {"username": username, "password": password}
    response = requests.post(USER_TOKEN_OBTAIN_URL, data=login_data)

    if response.status_code == 200:
        token = response.json()["access"]
        return token


def create_post(token, username, password):
    fake = Faker()
    post_data = {
        "title": fake.sentence(),
        "text": fake.paragraph(),
    }
    response = requests.post(
        CREATE_POST_URL, data=post_data, headers=get_headers(token)
    )
    if response.status_code == 401:
        new_token = login_user(username, password)
        response = requests.post(
            CREATE_POST_URL, data=post_data, headers=get_headers(new_token)
        )
    if response.status_code == 201:
        return response.json()["id"]


def like_post(post_id, token, username, password):
    like_post_url = f"{BASE_URL}posts/{post_id}/like/"
    response = requests.post(like_post_url, headers=get_headers(token))
    if response.status_code == 401:
        new_token = login_user(username, password)
        requests.post(like_post_url, headers=get_headers(new_token))


def run_bot():
    number_of_users, max_posts_per_user, max_likes_per_user = read_config()

    users = []
    post_ids = []

    for _ in range(number_of_users):
        username, password, token = create_user()

        if all((username, password, token)):
            users.append({"username": username, "password": password, "token": token})

        for _ in range(random.randint(1, max_posts_per_user)):
            post_id = create_post(token, username, password)

            if post_id is not None:
                post_ids.append(post_id)

    for user in users:
        for _ in range(random.randint(1, max_likes_per_user)):
            like_post(
                random.choice(post_ids),
                user["token"],
                user["username"],
                user["password"],
            )


if __name__ == "__main__":
    run_bot()
