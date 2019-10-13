from app import app
from csv import writer
from io import StringIO
import google_streetview.api
import json


def update_csv(model, file):
    data = StringIO()
    author = writer(data)
    # Write some rows
    for i, row in enumerate(file):
        if i == 0:
            address_index = row.index("Address")
            author.writerow(row + ["Predicted price"])
        else:
            address = row[address_index]
            predicted_price = predict_image(model=model, img=process_image(get_input(address)))
            author.writerow(row + [predicted_price])
    return data.getvalue()


def get_input(address):
    params = [{
        'size': '128x128',  # max 640x640 pixels
        'location': address,
        'heading': '0',
        'pitch': '-0.76',
        'key': app.config["STREETVIEW_KEY"]
    }]
    results = google_streetview.api.results(params)


def load_model():
    with open("model/model.json", "r") as json_file:
        architecture = json.load(json_file)
        model = model_from_json(json.dumps(architecture))
    model.load_weights("model/weights.h5")
    model.make_predict_function()
    return model


def process_image(img):
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.
    return img


def predict_image(model, img):
    processed_image = process_image(img)
    prediction = model.predict(img)
    return prediction
