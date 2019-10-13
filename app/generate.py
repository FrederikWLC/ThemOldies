from app import app
from csv import writer
from io import StringIO
from geopy.geocoders import Nominatim
import google_streetview.api
#from algorithm import model


def update_csv(file):
    data = StringIO()
    author = writer(data)
    # Write some rows
    for i, row in enumerate(file):
        if i == 0:
            address_index = row.index("Address")
            author.writerow(row + ["Predicted price"])
        else:
            address = row[address_index]
            #predicted_price = model.predict(get_input(address))
            author.writerow(row + [predicted_price])
    return data.getvalue()


def get_input():
    geolocator = Nominatim(user_agent="ThemOldies", timeout=None)
    coordinates = geolocator.latitude, geolocator.longitude
    params = [{
        'size': '250x250',  # max 640x640 pixels
        'location': str(coordinates),
        'heading': '0',
        'pitch': '-0.76',
        'key': app.config["STREETVIEW_KEY"]
    }]
    results = google_streetview.api.results(params)
