import requests
from sib_api_v3_sdk import TransactionalEmailsApi, ApiClient, Configuration

import requests

def get_weather_forecast(destination, trip_date):
    API_KEY = '745187ba5752d4c0e9be45a51441b8ea'  # Replace with your OpenWeather API key
    BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

    params = {
        'q': destination,
        'appid': API_KEY,
        'units': 'metric',
        'cnt': '40'  # Fetch weather data for the next 5 days (every 3 hours)
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_info = []
        for forecast in data['list']:
            # Match only the date part (YYYY-MM-DD) with the trip date
            if forecast['dt_txt'].startswith(trip_date):
                time = forecast['dt_txt'].split(" ")[1]  # Extract the time part
                temp = forecast['main']['temp']
                desc = forecast['weather'][0]['description']
                weather_info.append(f"At {time}, {desc} with {temp}°C")

        # If no matching forecast is found, return a meaningful message
        if not weather_info:
            return f"No specific weather data available for {trip_date}, but you can check general forecasts."

        return f"Weather forecast for {destination} on {trip_date}:\n" + "\n".join(weather_info)

    return "Could not retrieve weather data. Please try again later."

def send_weather_email(to_email, city, trip_date):
    weather_details = get_weather_forecast(city, trip_date)
    
    # Send the email with the weather details
    send_email_via_sendinblue(to_email, f"Weather Update for {city} on {trip_date}", weather_details)

def send_email_via_sendinblue(to_email, subject, content):
    api_key = 'Sendinblue Key'  # Replace with your actual API key

    # Configure the API client with your API key
    configuration = Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = TransactionalEmailsApi(ApiClient(configuration))

    sender = {"email": "rahulgupta160602@gmail.com"}
    recipient = [{"email": to_email}]
    html_content = f"<p>{content}</p>"
    send_smtp_email = {
        "sender": sender,
        "to": recipient,
        "subject": subject,
        "htmlContent": html_content
    }

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Weather email sent successfully: {api_response}")
    except Exception as e:
        print(f"Error sending email: {e}")
