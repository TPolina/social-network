# Social Network

DRF-based social network application.

## Features

- User signup/login.
- Read posts for every user and update/delete posts for post authors.
- Post liking/unliking for authenticated users.
- Analytics on likes amount during the given period.
- User profile and last activity.
- JWT authentication.
- Automated data filling bot.

## Installation

Python must be already installed

```shell
git clone git@github.com:TPolina/social-network.git
cd social_network
python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python3 bot/bot.py
```
