from app import app
from models import CarMake, CarModel
import requests
from database import db

def populate_database():
    # Getting makes and models from external database
    url = 'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?order=Make,Model&keys=Make,Model'
    headers = {
        'X-Parse-Application-Id': 'rn14Rlli0e5UxBexBLEAvkFyP01jDMs7GPvPBVNW', # This is your app's application id
        'X-Parse-REST-API-Key': '04aDgpOiqjxqHLeDXrRgPylnzdFXmJRuf2dcM5nQ' # This is your app's REST API key
    }

    all_data = []
    skip = 0
    limit = 1000

    while True:
        try:
            response = requests.get(f'{url}&limit={limit}&skip={skip}', headers=headers)
            data = response.json()['results']
            all_data.extend(data)

            if len(data) < limit:
                break
            skip += limit
        except requests.RequestException as e:
            print(f"An error occurred while fetching data: {e}")
            break  # Exit the loop if there's an error

    with app.app_context():
        for item in all_data:
            try:
                make_name = item["Make"]
                make = CarMake.query.filter_by(name=make_name).first()

                if not make:
                    make = CarMake(name=make_name)
                    db.session.add(make)

                model_name = item["Model"]
                car_model = CarModel(name=model_name, make_id=make.id)
                db.session.add(car_model)
            except Exception as e:
                print(f"An error occurred while processing make/model {make_name}/{model_name}: {e}")
                db.session.rollback()  # If there's an e

        try:
            db.session.commit()
        except Exception as e:
            print(f"An error occurred while saving to the database: {e}")
            db.session.rollback()


if __name__ == "__main__":
    populate_database()