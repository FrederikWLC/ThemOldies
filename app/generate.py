from csv import writer
from io import StringIO
from geopy.geocoders import Nominatim
import google_streetview.api


def update_csv(file):
    data = StringIO()
    author = writer(data)
    # Write some rows
    for row in file:
        author.writerow(row)
    return data.getvalue()


"""geolocator = Nominatim(user_agent="ThemOldies", timeout=None)
    print("Received a file")
    csvfile = list(csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=";"))
    address_index = csvfile[0].index("Addresses")
    csvfile[0].append("Predicted Prices")
    updated_csv = ""
    for i, row in enumerate(csvfile):

        if row is None:
            break
        address = row[address_index]
        location = "location"
        if location:
            predicted_price = "$"
        else:
            predicted_price = "N/A"
            row.append(predicted_price)
            updated_csv += ";".join(row) + "\n" """
