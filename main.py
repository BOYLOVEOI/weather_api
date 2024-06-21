# Import Statements
from flask import Flask, render_template
import pandas as pd
import numpy as np
from datetime import datetime

# Creating a Flask Object to manage website
app = Flask(__name__)

# Creating a route (URL): [domain]/ so that whenevers users first enter our
# site the home.html will be the first page they see
@app.route("/")
def home():
    # returning and rendering the home.html file
    return render_template("home.html")

# Creating another route for the api
# the <> symbols in <station> and <date> denote to Flask that users can
# enter their own values in these placeholders which are held in the 
# variables (of the same name) in the decorator 
@app.route("/api/v1/<station>/<date>")
def api(station, date):
    # Since we can't preload and read ALL data files, we will only read the file
    # of the station the user wants
    # Creating fileName to pass in
    fileName = f'data_small\TG_STAID{station.zfill(6)}.txt'
    # Creating the dataframe with the skiprows and parse_dates arguments
    df = pd.read_csv(fileName, skiprows=20, parse_dates= ['    DATE'])
    
    # Creating new columns of the dataframe to remove dummy values (-9999) 
    # and retrieve actual avg temp
    df['TG0'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    df['TG'] = df['TG0'] / 10

    # Creating new column for fahrenheit
    df['Fahrenheit'] = df['TG'] * (9/5) + 32

    # Creating date variable 
    # Use the datetime.strptime() method to format the string into a datetime format and retrieve ONLY the date (.date())
    # Format the datetime date object into a str 
    date_formatted = str(datetime.strptime(date, '%Y%m%d').date())
    
    # Creating temperature variable to store temp
    # Using the .loc[] method to set retrieve the avg temperature based on user inputted date 
    temperature = df.loc[df['    DATE'] == date_formatted]['TG'].squeeze()
    # Creating fahrenheit variable
    fahrenheit = df.loc[df['    DATE'] == date_formatted]['Fahrenheit'].squeeze()
 
    # Return JSON of the station, date, and the temperature
    return {"station": station,
            "date": date_formatted,
            "temp (in C)": temperature,
            "temp (in F)": fahrenheit}

if __name__ == "__main__":
    # Running the website with debug ON
    app.run(debug=True)