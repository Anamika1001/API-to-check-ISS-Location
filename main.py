import requests
from datetime import *
import smtplib
import time

MY_LAT=22.638333
MY_LONG=88.375687
UserId=input("Enter your email id: ")
UserPassword=input("Enter your password: ")

def iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    Error=response.raise_for_status()
    data=response.json()
    iss_latitude=float(data["iss_position"]["latitude"])
    iss_longitude=float(data["iss_position"]["longitude"])

    if MY_LAT -5 <= iss_latitude <= MY_LAT+5 and MY_LONG -5 <= iss_longitude <= MY_LONG+5:
        return True
def Is_night():
    parameters={
        "lat":MY_LAT,
        "lng":MY_LONG,
        "formatted":0,
    }

    response_sunset=requests.get("http://api.sunrise-sunset.org/json",params=parameters)
    sun_data=response_sunset.json()
    sunrise=int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset=int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now=datetime.now()
    hour=time_now.hour
    if hour>=sunset or hour<=sunrise:
        return True

while True:
    time.sleep(90)
    if iss_overhead() and Is_night():
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=UserId,password=UserPassword)
            connection.sendmail(from_addr=UserId,to_addrs=UserId,msg=f"Subject:Look Up\n\nISS is above you in the sky")

