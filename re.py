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

        if is_ideal:
            send_email_alert("The weather is ideal for photography!")
        else:
            print("\nPhotography Alert: The weather might not be the best for photography.")

    else:
        print(f"Error: {response.status_code}, {response.text}")


def send_email_alert(message):
    yag = yagmail.SMTP("your_email@gmail.com", "your_email_password")
    yag.send(
        to="your_email@gmail.com",
        subject="Photography Weather Alert",
        contents=message,
    )
    print("Email alert sent!")


if __name__ == "__main__":
    api_key = input("YOUR_API_KEY_HERE")
    city = input("Enter the city name: ")
    get_weather(api_key, city)
import yagmail

def send_email(to_email, subject, contents):
  try:
    yag = yagmail.SMTP("", "")
    yag.send(to=to_email, subject=subject, contents=contents)
    print("Email sent successfully!")
  except Exception as e:
    print(f"Error sending email: {e}")

if __name__ == "__main__":
    recipient_email = input("Enter recipient's email address: ")
    email_subject = input("Enter the email subject: ")
    email_body = input("Enter the email content: ")

    send_email(recipient_email, email_subject, email_body)

    camera = camera_api.connect()



    if is_ideal:

        camera_api.set_aperture(camera, suggested_settings["Aperture"])
        camera_api.set_shutter_speed(camera, suggested_settings["Shutter Speed"])
        camera_api.set_iso(camera, suggested_settings["ISO"])