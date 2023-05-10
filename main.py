import requests
from datetime import datetime
import smtplib
import time


MY_LAT = "YOUR LATITUDE"
MY_LONG = "YOUR LONGITUDE"
MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"
RECEIVER_EMAIL = "RECEIVER EMAIL"


def iss_is_over():
    """Returns True when your position is within +5 or -5 degrees of the ISS position."""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    """Returns True if there's after sunset and before sunrise at the moment."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if sunrise >= time_now >= sunset:
        return True


def send_email():
    with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS", 587, timeout=120) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=RECEIVER_EMAIL,
                    msg=f"Subject: ISS near your location! "
                        f"\n\nThe ISS is near your current location at the moment. "
                        f"\nLook up at the sky and find it above your head!"
        )


while True:
    time.sleep(10)
    if iss_is_over() and is_night():
        send_email()
