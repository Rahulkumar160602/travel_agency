import openpyxl
import os
from datetime import datetime
from django.conf import settings

# Save user data to Excel
def save_user_to_excel(email, phone, password):
    file_path = os.path.join(settings.BASE_DIR, "storage", "user_data.xlsx")
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        signup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append([email, phone, password, signup_date])
        workbook.save(file_path)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Get user data from Excel
def get_user_data_from_excel(email):
    file_path = os.path.join(settings.BASE_DIR, "storage", "user_data.xlsx")
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=2):  # Skip header row
            # Check if the row has at least 3 columns and match the email
            if len(row) >= 3 and row[0].value == email:
                return {
                    'email': row[0].value,
                    'phone': row[1].value,
                    'password': row[2].value,
                    'timestamp': row[3].value if len(row) > 3 else None,  # Add timestamp if it exists
                }
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


import openpyxl
from django.conf import settings
import os

# Save user profile data to Excel
def save_user_profile_to_excel(email, name, address, dob, gender, preferences, budget, linkedin, instagram, travel_history, profile_picture_url):
    file_path = os.path.join(settings.BASE_DIR, 'storage', 'user_data.xlsx')
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # Find the user and update their data
        for row in sheet.iter_rows(min_row=2):  # Skip header row
            if row[0].value == email:
                row[3].value = name
                row[4].value = address
               
                workbook.save(file_path)
                return True
        return False
    except Exception as e:
        print(f"Error saving user profile: {e}")
        return False



import os
import openpyxl

# Get the base directory of the app
from datetime import datetime

def save_booking_to_excel(name, email, destination, date, guests, notes):
    # Absolute path to the bookings.xlsx file
    file_path = os.path.join(settings.BASE_DIR, "travel_app", "storage", "bookings.xlsx")

    try:
        # Check if the Excel file exists
        if not os.path.exists(file_path):
            # Create a new Excel file with headers
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Name", "Email", "Destination", "Travel Date", "Guests", "Notes", "Booking Time"])
        else:
            # Load the existing Excel file
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

        # Add the booking data with a timestamp
        booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append([name, email, destination, date, guests, notes, booking_time])

        # Save the changes
        workbook.save(file_path)
        print("Booking data saved successfully!")  # Debug message
        return True
    except Exception as e:
        print(f"Error saving booking to Excel: {e}")
        return False

import openpyxl
import os
from datetime import datetime
from django.conf import settings

def save_contact_to_excel(name, email, message):
    # Absolute path to the user_data.xlsx file
    file_path = os.path.join(settings.BASE_DIR, "travel_app", "storage", "contact.xlsx")
    
    # Log the file path being used
    print(f"File Path: {file_path}")
    
    try:
        # If the file doesn't exist, create a new one and add headers
        if not os.path.exists(file_path):
            print("File does not exist. Creating a new file.")
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Name", "Email", "Message", "Signup Date"])  # Add headers
            workbook.save(file_path)

        # If the file is corrupted, delete it and create a new one
        if file_path.endswith(".xlsx"):
            with open(file_path, 'rb') as f:
                if not f.read(4) == b"PK\x03\x04":
                    print("File is corrupted. Re-creating the file.")
                    os.remove(file_path)  # Remove the corrupted file
                    workbook = openpyxl.Workbook()
                    sheet = workbook.active
                    sheet.append(["Name", "Email", "Message", "Signup Date"])  # Add headers
                    workbook.save(file_path)

        # Load the Excel file
        print("Loading the workbook.")
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # Add the user's data to the sheet
        signup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Appending data: {name}, {email}, {message}, {signup_date}")
        sheet.append([name, email, message, signup_date])

        # Save the changes
        print("Saving the workbook.")
        workbook.save(file_path)
        return True
    except Exception as e:
        print(f"Error saving user to Excel: {e}")  # Print the full exception
        return False
import pandas as pd
import requests

# Read booking data from the Excel sheet
def get_booking_data():
    file_path = r'C:\travel_agency\travel_agency\travel_app\storage\bookings.xlsx'
    df = pd.read_excel(file_path)

    # Assuming the data has columns like 'User', 'BookingDate', 'TripDate', 'Destination'
    bookings = df.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    return bookings


# Get weather data for the user's destination and trip date
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
            if forecast['dt_txt'].startswith(str(trip_date)):

                time = forecast['dt_txt'].split(" ")[1]  # Extract the time part
                temp = forecast['main']['temp']
                desc = forecast['weather'][0]['description']
                weather_info.append(f"At {time}, {desc} with {temp}°C")

        # If no matching forecast is found, return a meaningful message
        if not weather_info:
            return f"No specific weather data available for {trip_date}, but you can check general forecasts."

        return f"Weather forecast for {destination} on {trip_date}:\n" + "\n".join(weather_info)

    return "Could not retrieve weather data. Please try again later."
