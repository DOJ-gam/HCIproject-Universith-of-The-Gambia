from flask import redirect, render_template, flash, request, url_for
import requests
from packages import app
import json
# import datetime

data = json.load(open("data.json"))


# Gambia
req = requests.get("https://disease.sh/v3/covid-19/countries/gambia")
gambia = req.json()

# Global Data
req = requests.get("https://disease.sh/v3/covid-19/all")
global_data = req.json()

# All countries data
req = requests.get("https://disease.sh/v3/covid-19/countries")
all_countries_data = req.json()

# Africa
req = requests.get("https://disease.sh/v3/covid-19/continents/africa")
africa = req.json()

# Europe
req = requests.get("https://disease.sh/v3/covid-19/continents/europe")
europe = req.json()

# Asia
req = requests.get("https://disease.sh/v3/covid-19/continents/asia")
asia = req.json()

# North America
req = requests.get(f"https://disease.sh/v3/covid-19/continents/north america")
north_america = req.json()

# South America
req = requests.get(f"https://disease.sh/v3/covid-19/continents/south america")
south_america = req.json()

# All of America
america = {
            "cases": north_america['cases'] + south_america['cases'],
            "population": north_america['population'] + south_america['population'],
            "critical": north_america['critical'] + south_america['critical'],
            "todayRecovered": north_america['todayRecovered'] + south_america['todayRecovered'],
            "deaths": north_america['todayDeaths'] + south_america['todayDeaths'],
            "todayCases": north_america['todayCases'] + south_america['todayCases'],
            "active": north_america['active'] + south_america['active'],
            "recovered": north_america['recovered'] + south_america['recovered'],
            "tests": north_america['tests'] + south_america['tests'],
            "countries": north_america['countries'] + south_america['countries'],
            "todayDeaths": north_america['todayDeaths'] + south_america['todayDeaths'],
        }


# date and time
# timestamp = datetime.datetime.fromtimestamp(1500000000)
# print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home Page", gambia=gambia, global_data=global_data, all_countries=all_countries_data, africa=africa, asia=asia, europe=europe, america=america, south_america=south_america, north_america=north_america)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/global")
def allCountries():
    return render_template("global.html", title="Global Statistics", all_countries=all_countries_data, global_data=global_data)


@app.route('/countries/<country>')
def country(country):
    try:

        # have to use the 'f' to be able to insert '{}'
        req = requests.get(
            f"https://disease.sh/v3/covid-19/countries/{country}")

        data = req.json()

        return render_template('country.html', country=data)

    except Exception as error:
        print('There is an error', error)
        return "There is an error " + error
        return "data for a {country}"


@app.route('/continents/<continent>')
def continent(continent):

    # Data for continents
    if continent == 'america':
     
        continent_stats = america
    else:
        req = requests.get(
            f"https://disease.sh/v3/covid-19/continents/{continent}")

        continent_stats = req.json()

    all_continent_data = []

#       for every country in all the countries, if the continent is in the all_countries_data as continent, add to the list
    # we use in because america is in north america, and south america
    for country in all_countries_data:
        if continent in country['continent'].lower():
            all_continent_data.append(country)

    return render_template('continents.html', all_continent_data=all_continent_data, continent_stats=continent_stats, page_title=continent)


@app.route('/search')
def search():
    # country here is what the user entered in the form input
    country = request.args.get('country')

    # Filtering starts here...
    filtered_data = []

    for record in all_countries_data:
        # we are converting country to lowercase and check if the word is in the name of the country in the covid-data list.
        if country.lower() in record['country'].lower():
            filtered_data.append(record)

    return render_template('search.html', global_data=global_data, all_countries=filtered_data, gambia=gambia,  title="Search Result for "+country)


@app.route("/contact", methods=['GET', 'POST'])
def contactMe():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['message']

        subject = "Name: "+name+".......   Email: " + \
            email+".........   Contact: " + phone
        recipient = "dojclientmail@gmail.com"
        message = Message(
            subject, sender="dojservermail@gmail.com", recipients=[recipient])
        message.body = msg
        mail.send(message)
        success = "Message Sent"

    # return home()
    return redirect(url_for("home"))