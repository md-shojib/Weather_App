from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class City(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
# with app.app_context():
#     db.create_all()
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        city_name = request.form['city']

        new_city = City(name=city_name)
        db.session.add(new_city)
        db.session.commit()
        return redirect('/')
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=bb24995818cca884bf0d521a32330a4c"
    cities = City.query.all()
    weather_list=[]
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        if r['cod'] !='404':
            weather = {
                'city' : city.name,
                'temparature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon']
            }
            weather_list.append(weather)
    return render_template('index.html', weather_list=weather_list)
if __name__ == '__main__':
    app.run(debug=True, port=8000)