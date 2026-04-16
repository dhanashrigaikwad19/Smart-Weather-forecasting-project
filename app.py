from flask import Flask,render_template,request,redirect,url_for,session
import requests
app = Flask(__name__)
app.secret_key = "mysecret123"

API_KEY = "8b453f8afc61ff0f610efec0616fbb43"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# -----------------------------
# Fetch Weather Data
# -----------------------------
def get_weather(city):
    params = {"q": city, "appid":API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    print(response.json())
    return response.json()

# -----------------------------
# 🧍 Personal Suggestions
# -----------------------------
def suggestions(temp, humidity, weather, wind):
    tips = []

    if temp > 35:
        tips.append("🔥 Very hot! Drink water & avoid sun.")
    elif temp < 15:
        tips.append("🧥 Cold weather. Wear warm clothes.")

    if weather.lower() == "rain":
        tips.append("☔ Carry an umbrella.")
    elif weather.lower() == "clear":
        tips.append("😎 Good for outdoor activities.")

    if humidity > 80:
        tips.append("💧 High humidity. Stay cool.")
    elif humidity < 30:
        tips.append("🌵 Dry weather. Use moisturizer.")

    if wind > 10:
        tips.append("🌬️ Strong wind. Travel carefully.")

    if not tips:
        tips.append("😊 Weather is normal.")

    return " | ".join(tips)

# -----------------------------
# 🌾 Farmer Alert System
# -----------------------------
def farmer_alert(temp, humidity, weather):
    alerts = []

    if weather.lower() == "rain":
        alerts.append("🌾 Rain expected. Avoid irrigation.")
    if temp > 35:
        alerts.append("🌾 High temperature. Protect crops.")
    if humidity < 30:
        alerts.append("🌾 Low moisture. Irrigation needed.")
    if humidity > 85:
        alerts.append("🌾 High humidity. Risk of disease.")

    if not alerts:
        alerts.append("🌾 Conditions are favorable.")

    return " | ".join(alerts)

# -----------------------------
# 🧠 Prediction Logic
# -----------------------------
def predict(temp, humidity):
    if humidity > 70 and temp > 25:
        return "🔮 High chance of rain tomorrow."
    elif temp > 35:
        return "🔮 Tomorrow may be very hot."
    else:
        return "🔮 Weather likely stable."

# -----------------------------
# Main Route
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open("users.txt", "r") as f:
            users = f.readlines()

        for user in users:
            u, p = user.strip().split(",")
            if u == username and p == password:
                session["user"] = username
                return redirect(url_for("index"))

        return render_template("login.html", error="Invalid Login")

    return render_template("login.html")
 
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open("users.txt", "a") as f:
            f.write(username + "," + password + "\n")

        return redirect("/login")

    return render_template("signup.html")          
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    weather_data = None

    if request.method == "POST":
        city = request.form["city"]
        data = get_weather(city)

        if data and data.get("main"):
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["main"]
            wind = data["wind"]["speed"]

            weather_data = {
                "city": city,
                "temp": temp,
                "humidity": humidity,
                "condition": condition,
                "wind": wind,
                "suggestion": suggestions(temp, humidity, condition, wind),
                "farmer": farmer_alert(temp, humidity, condition),
                "prediction": predict(temp, humidity)
            }
    return render_template("index.html",weather=weather_data)



if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0",port=10000)
    

