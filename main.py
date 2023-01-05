import requests
from datetime import datetime
from os import environ

nutritionix_exercise_api = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutritionix_app_id = environ.get('APP_ID')
nutritionix_app_key = environ.get('APP_KEY')

sheety_add_row_api = "https://api.sheety.co/534704e14519d386a9d81a1f131dd383/myWorkouts/sheet1"

nutritionix_headers = {
    'x-app-id': nutritionix_app_id,
    'x-app-key': nutritionix_app_key,
}

exercise_params = {
    'query': input('Tell us what did you do today: '),
    'gender': 'male',
    'weight_kg': 55,
    'height_cm': 178,
    'age': 22

}

response = requests.post(url=nutritionix_exercise_api, headers=nutritionix_headers, json=exercise_params)
response.raise_for_status()
data_taken = response.json()


sheety_headers = {
    'Authorization': f'Bearer {environ.get("BEARER_TOKEN")} ',
    'Content-Type': 'application/json',
}

for exercise in data_taken['exercises']:

    exercise_name = exercise['name']
    calories_burnt = exercise['nf_calories']
    duration = exercise['duration_min']

    sheety_params = {
        'sheet1': {
            'date': datetime.now().strftime('%d/%m/%Y'),
            'time': datetime.now().strftime('%X'),
            'exercise': exercise_name.title(),
            'duration': duration,
            'calories': calories_burnt,

        }

    }

    sheety_response = requests.post(url=sheety_add_row_api,
                                    json=sheety_params,
                                    headers=sheety_headers)
    print(sheety_response.text)

