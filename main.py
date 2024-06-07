# Import Statements
from flask import Flask, render_template

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
    temperature = 23
    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    # Running the website with debug ON
    app.run(debug=True)