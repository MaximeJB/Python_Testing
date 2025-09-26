import json
from flask import Flask,render_template,request,redirect,flash,url_for, abort
from email.utils import parseaddr
from datetime import datetime
import pdb 


def is_valid_email(email):
    return "@" in parseaddr(email)[1]


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    
    if not is_valid_email(email) or not email:
        flash("Invalid email format or email not found")
        return redirect(url_for('index'))
    
    clubs = loadClubs()

    try:
        club = [club for club in clubs if club['email'].lower() == email.lower()][0]
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]


    place_asked = int(request.form['places'])
    number_of_place = int(competition['numberOfPlaces'])
    points = int(club['points'])
    booked = club.get('booked',0)
    comp_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")

    if place_asked > points or place_asked <= 0:
        abort(400, description="Not enough points to book !")
    if place_asked > number_of_place or place_asked > 12 :
        abort(400, description="Not enough places available")
    if booked + place_asked > 12:
        abort(400, description="Too many places already booked !")
    if comp_date < datetime.now():
        abort(400, description="Cannot book past competition")

    competition['numberOfPlaces'] = number_of_place - place_asked
    club['points'] = points - place_asked
    club['booked'] = club.get('booked', 0) + place_asked
    flash('Great-booking complete!')

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)