from app import app
from csv import writer
from io import StringIO, BytesIO
import numpy as np
import google_streetview.api
import json
import requests
from PIL import Image
from keras.models import model_from_json
from keras.preprocessing import image
from os import path


def update_csv(model, file):
    data = StringIO()
    author = writer(data, delimiter=";")
    # Write some rows
    for i, row in enumerate(file):
        if i == 0:
            address_index = row.index("Address")
            author.writerow(row + ["Predicted price"])
        else:
            address = row[address_index]
            #predicted_price = predict(model, address)
            predicted_price = "N/A"
            author.writerow(row + [predicted_price])
        print(i)
    return data.getvalue()


def get_input(address):
    params = [{
        'size': '128x128',
        'location': address,
        'key': app.config["STREETVIEW_KEY"]
    }]
    results = google_streetview.api.results(params)
    if results.metadata[0]["status"] != "OK":
        return None
    response = requests.get(results.links[0]).content
    img = np.expand_dims(image.img_to_array(Image.open(BytesIO(response))), axis=0) / 255.
    return img


def load_model():
    basedir = path.abspath(path.dirname(__file__))
    with open(path.join(basedir, "model/model.json"), "r") as json_file:
        architecture = json.load(json_file)
        model = model_from_json(json.dumps(architecture))
    model.load_weights(path.join(basedir, "model/weights.h5"))
    model._make_predict_function()
    return model


def predict(model, address):
    img = get_input(address)
    if img:
        return model.predict(img)
    return "N/A"
