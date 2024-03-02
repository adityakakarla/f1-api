from flask import Flask
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
import os

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
load_dotenv()
user = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

users = {
    user: password
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

class Schedule(Resource):
    @auth.login_required
    def get(self):
        url = 'https://www.formula1.com/en/racing/2024.html'
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
        else:
            html_content = ''

        soup = BeautifulSoup(html_content, 'html.parser')

        elements = soup.find_all(class_ = 'col-12 col-sm-6 col-lg-4 col-xl-3')

        race_info = {}

        for element in elements:
            location = element.find(class_ ="event-place").text
            name = element.find(class_ = "event-title f1--xxs").text

            race_info[len(race_info)] = {
                'name': name.strip().title(),
                'location': location.strip(),
            }

        return race_info, 200
        

api.add_resource(Schedule, "/schedule")

if __name__ == "__main__":
    app.run()