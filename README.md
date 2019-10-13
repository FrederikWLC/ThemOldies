# ThemOldies

To run the program, first install the packages by typing this line into your console with the current directory being the one that contains this application.
```
pip install -r requirement.txt
```
Then type in this command
```
flask run --without-threads
```
You can then register, subscribe and upload a csv file including addresses in a collumn called, "Address". And you will be able to download an updated version of that file including price predictions of the property on these addresses.

As an example csv file, you can make use of the example provided in this repository, called "example_input.csv".

***This app is not yet complete because of errors in terms of communication between client and server and communication between server and the google streetview api. Therefore all it does for now is providing the user with price predictions of 'N/A'.***
