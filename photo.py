import requests
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_weather(city, api_key):
    """Fetches weather data for a given city using the OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Get temperature in Celsius by default
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def suggest_camera_settings(weather_data):
    """Suggests camera settings based on weather conditions."""
    description = weather_data["weather"][0]["description"]
    visibility = weather_data["visibility"] / 1000  # Convert meters to kilometers

    settings = {
        "ISO": None,
        "Aperture": None,
        "Shutter Speed": None,
        "White Balance": None,
        "Other Tips": []
    }

    # General recommendations based on weather description
    if "clear" in description.lower():
        settings["ISO"] = 100  # Low ISO for bright conditions
        settings["Aperture"] = "f/8 - f/11"  # Moderate aperture for sharpness
        settings["White Balance"] = "Daylight"
        if visibility > 10:  # Good visibility
            settings["Shutter Speed"] = "1/250 - 1/500"
            settings["Other Tips"].append("Consider using a polarizing filter to reduce glare and enhance colors.")
        else:  # Reduced visibility (e.g., haze or fog)
            settings["Shutter Speed"] = "1/125 - 1/250"
            settings["Other Tips"].append("Use a wider aperture to let in more light.")

    elif "clouds" in description.lower():
        settings["ISO"] = 200 - 400  # Slightly higher ISO for less light
        settings["Aperture"] = "f/5.6 - f/8"
        settings["White Balance"] = "Cloudy"
        settings["Other Tips"].append("Experiment with different shutter speeds to capture the movement of clouds.")

    elif "rain" in description.lower() or "drizzle" in description.lower():
        settings["ISO"] = 400 - 800
        settings["Aperture"] = "f/4 - f/5.6"
        settings["White Balance"] = "Auto"
        settings["Other Tips"].append("Use a faster shutter speed to freeze raindrops.")
        settings["Other Tips"].append("Consider using a rain cover to protect your camera.")

    elif "snow" in description.lower():
        settings["ISO"] = 100 - 200
        settings["Aperture"] = "f/8 - f/11"
        settings["White Balance"] = "Cloudy"
        settings["Other Tips"].append("Adjust exposure compensation to avoid underexposing the snow.")
        settings["Other Tips"].append("Protect your camera from moisture and cold temperatures.")

    else:  # Other weather conditions (e.g., thunderstorm, mist)
        settings["ISO"] = "Auto"
        settings["Aperture"] = "f/5.6 - f/8"
        settings["White Balance"] = "Auto"
        settings["Other Tips"].append("Experiment with different settings to find what works best.")

    return settings

def send_weather_email(to_email, city, weather_data):
    """Sends an email with weather information and camera setting suggestions."""
    from_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")

    if not from_email or not password:
        print("Error: Email credentials not found in environment variables.")
        return

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"Weather in {city} and Camera Settings"

    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    camera_settings = suggest_camera_settings(weather_data)

    body = f"""
    The weather in {city} is {description} with a temperature of {temperature}°C.

    Recommended camera settings:
    """

    for setting, value in camera_settings.items():
        if setting == "Other Tips" and value:
            body += "\nAdditional tips:\n"
            for tip in value:
                body += f"- {tip}\n"
        else:
            body += f"- {setting}: {value}\n"

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Adjust for your email provider
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

# Get API key from environment variable
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
if not api_key:
    print("Error: OPENWEATHERMAP_API_KEY not found in environment variables.")
    exit(1)

# Prompt user for city and recipient email
city_name = input("Enter the city name you want weather information for: ")
to_email = input("Enter the email address to send the weather information to: ")

# Fetch weather data and send email if successful
weather_data = get_weather(city_name, api_key)

if weather_data:
    send_weather_email(to_email, city_name, weather_data)
else:
    print("Unable to fetch weather data. Email not sent.")