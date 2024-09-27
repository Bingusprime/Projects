import requests
import yagmail

def get_weather(api_key, city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"


    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()

        city_name = data['name']
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']

        print(f"City: {city_name}")
        print(f"Temperature: {temperature}°C")
        print(f"Weather: {weather_description}")


        is_ideal = False
        if (
            20 <= temperature <= 25
            and "clear" in weather_description.lower()
            and 3 <= data["visibility"] / 1000 <= 10
        ):
            is_ideal = True




import yagmail


import requests
import yagmail

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        temperature = round(data["main"]["temp"] - 273.15, 1)
        weather_description = data["weather"][0]["description"]
        visibility = data["visibility"] / 1000

        is_ideal = False
        if (
            20 <= temperature <= 25
            and "clear" in weather_description.lower()
            and 3 <= visibility <= 10
        ):
            is_ideal = True

        if is_ideal:
            send_email_alert("The weather is ideal for photography!")
        else:
            print("\nPhotography Alert: The weather might not be the best for photography.")

    else:
        print(f"Error: {response.status_code}, {response.text}")




def send_email_alert(message):
    try:
        yag = yagmail.SMTP("zmanfungle@gmail.com", "fmjp dvou cnwz opsk")
        yag.send(
            to="mattbusel@gmail.com",
            subject="Photography Weather Alert",
            contents=message,
        )
        print("Email alert sent!")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    api_key = input("Enter your OpenWeatherMap API key: ")
    city = input("Enter the city name: ")
    get_weather(api_key, city)


if __name__ == "__main__":
    recipient_email = input("Enter recipient's email address: ")


    if "@" not in recipient_email or "." not in recipient_email:
        print("Invalid email address. Please enter a valid email.")
    else:
        email_subject = input("Enter the email subject: ")
        email_body = input("Enter the email content: ")





def get_weather_data():
    api_key = "YOUR_API_KEY"
    city = "Yonkers,US"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        weather = data["weather"][0]["main"]  # Get overall weather condition
        brightness = data["clouds"]["all"]  # Cloudiness as a proxy for brightness (0-100)
        rain = data["rain"]["1h"] if "rain" in data else 0  # Rainfall in the last hour (mm)
        visibility = data["visibility"] / 1000  # Visibility in kilometers

        return {
            "weather": weather,
            "brightness": brightness,
            "rain": rain,
            "visibility": visibility
        }
    else:
        print("City not found.")
        return None


        def translate_weather_to_settings(weather_data):
            new_settings = {}

            def translate_weather_to_settings(weather_data):
                new_settings = {}

                if weather_data is None:  # Handle case where weather data is unavailable
                    return new_settings

                    # Brightness adjustments
                if weather_data["brightness"] < 30:
                    new_settings["ISO"] = 100
                    new_settings["Shutter Speed"] = 1 / 250
                elif weather_data["brightness"] < 70:
                    new_settings["ISO"] = 200
                    new_settings["Shutter Speed"] = 1 / 125
                else:  # Cloudy or dark conditions
                    new_settings["ISO"] = 400
                    new_settings["Shutter Speed"] = 1 / 60

                # Rain adjustments
                if weather_data["rain"] > 0:
                    new_settings["Image Stabilization"] = "On"
                    new_settings["White Balance"] = "Cloudy"


                if weather_data["visibility"] < 1:
                    new_settings["Contrast"] = "High"
                    new_settings["Focus Mode"] = "Manual"

                return new_settings
            return new_settings


        def apply_settings_to_camera(new_settings):
            try:
                camera = nc.connect_to_camera()
                current_settings = nc.get_current_settings(camera)


                updated_settings = {**current_settings, **new_settings}

                nc.apply_settings(camera, updated_settings)
                print("Camera settings updated successfully!")

            except Exception as e:
                print(f"Error applying settings: {e}")
            finally:
                nc.disconnect_from_camera(camera)


        if __name__ == "__main__":
            while True:
                weather_data = get_weather_data()
                new_settings = translate_weather_to_settings(weather_data)
                apply_settings_to_camera(new_settings)


                time.sleep(600)  # Example: Update every 10 minutes