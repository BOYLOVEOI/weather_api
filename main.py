# Import Statements
from flask import Flask, render_template
import pandas as pd
import numpy as np
from datetime import datetime

# Creating a Flask Object to manage website
app = Flask(__name__)

# Holding stations dataframe to display onto home page
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
# Only having the dataframe hold the station ID and station name
stations = stations[["STAID", "STANAME                                 "]]

# Creating a route (URL): [domain]/ so that whenevers users first enter our
# site the home.html will be the first page they see
@app.route("/")
def home():
    # returning and rendering the home.html file
    return render_template("home.html", data=stations[["STAID", "STANAME                                 "]].to_html())

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
    
    # Removing dummy values (-9999) 
    df['   TG'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    # Retrieving actual temperatures (since temp values are multiplied by 10)
    df['   TG'] = df['   TG'] / 10

    # Creating new column for fahrenheit
    df['Fahrenheit'] = (df['   TG'] * (9/5) + 32).round()

    # Creating date variable 
    # Use the datetime.strptime() method to format the string into a datetime format and retrieve ONLY the date (.date())
    # Format the datetime date object into a str 
    date_formatted = str(datetime.strptime(date, '%Y%m%d').date())
    
    # Creating temperature variable to store temp
    # Using the .loc[] method to retrieve the avg temperature based on user inputted date 
    temperature = df.loc[df['    DATE'] == date_formatted]['   TG'].squeeze()
    # Creating fahrenheit variable
    fahrenheit = df.loc[df['    DATE'] == date_formatted]['Fahrenheit'].squeeze()
 
    # Return JSON of the station, date, and the temperature
    return {"station": station,
            "date": date_formatted,
            "temp (in C)": temperature,
            "temp (in F)": fahrenheit}

# Adding another route if the user ONLY inputs the station (then historical data for the station is returned)
@app.route("/api/v1/<station>")
def all_data(station):
    # Retrieve filename
    fileName = f'data_small/TG_STAID{station.zfill(6)}.txt'
    # Read the file
    df = pd.read_csv(fileName, skiprows=20, parse_dates= ['    DATE'])
    # Transform invalid data
    df['   TG'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    # Transform temperature (as actual temperature in df is multipled by 10)
    df['   TG'] = df['   TG'] /  10
    # Creating fairenheit column
    df['Fairenheit'] = (df['   TG'] * (9/5) + 32).round()
    # Change dataframe to dict so we can pass entire dataframe back to API
    results = df.to_dict(orient="records")
    return results

# Adding another route if the user inputs the station and the YEAR
@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    # Retrieve filename
    fileName = f'data_small/TG_STAID{station.zfill(6)}.txt'
    # Read the file
    df = pd.read_csv(fileName, skiprows=20)
    # Transforming invalid data
    df['   TG'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    # Transform temperature (as actual temperature in df is multipled by 10)
    df['   TG'] = df['   TG'] /  10
    # Creating fairenheit column
    df['Fairenheit'] = (df['   TG'] * (9/5) + 32).round()
    # Converting the Date column to string, so we can use the str.startswith() method
    # .astype() allows us to change the values of a column to a certain data type 
    df['    DATE'] = df['    DATE'].astype(str)   
    # Create new dataframe that ONLY holds the records for a certain year
    # You can create a new dataframe by passing in a condition (our condition is that the resulting dataframe holds
    # records that start with the year passed in by the user)
    results = df[df["    DATE"].str.startswith(str(year))]
    # Convert the dataframe that holds only year records into a dict
    results = results.to_dict(orient="records")
    # Return results
    return results

if __name__ == "__main__":
    # Running the website with debug ON
    app.run(debug=True)