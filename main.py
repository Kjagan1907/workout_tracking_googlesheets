import requests
import datetime
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()  # Automatically reads .env in project folder
load_dotenv(dotenv_path="tokens.env")  # <-- specify your file

APP_ID = os.getenv('MY_NUTRI_APP_ID')
API_KEY = os.getenv('MY_NUTRI_API_KEY')
USER_ID = os.getenv('MY_SHEETY_USER_ID')

PASSWORD = os.getenv('MY_SHEETY_PASSWORD')



excercise_input = input(f"Tell me which Excercises you did:")

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
  }

parameters = {
    'query': excercise_input
}

response = requests.post(url='https://trackapi.nutritionix.com/v2/natural/exercise',headers=headers, json=parameters)
print(response.json())

sheety_endpoint = 'https://api.sheety.co/263372a94591de31d0d4d5779b3b563f/myWorkouts/workouts'
sheety_authenication = HTTPBasicAuth(USER_ID, PASSWORD) 

today_date = datetime.datetime.now().strftime("%d/%m/%Y")
now_time = datetime.datetime.now().strftime("%X")

print(now_time)
data = response.json()
all_excercises = [name['name'] for name in data['exercises']]
all_calories = [cal['nf_calories'] for cal in data['exercises']]
all_duration = [dur['duration_min'] for dur in data['exercises']]
print(all_excercises)
print(all_calories)
print(all_duration)

for i in range(len(all_excercises)):
  sheety_parameters = {
      'workout': {
          'date': today_date,
          'time': now_time,
          'exercise': all_excercises[i],
          'duration': all_duration[i],
          'calories': all_calories[i],
      }
  }
  sheety_response = requests.post(url=sheety_endpoint, json=sheety_parameters, auth=sheety_authenication)
  print(sheety_response.text)