from django.shortcuts import render,HttpResponse


def homepage(request):
    return render(request, 'Homepage.html')
# Create your views here.
def services(request):
    return render(request, 'Services.html')

# Create your views here.
def contact(request):
    return render(request, 'Contact.html')
# Create your views here.

def destinations(request):
    return render(request, 'Destinations.html')
# Create your views here.
def trip_planing(request):
    return render(request, 'trip_planing.html')

def custom_itineraries(request):
    return render(request, 'custom_itineraries.html')

def group_discounts(request):
    return render(request, 'group_discounts.html')

def travel_insurance(request):
    return render(request, 'travel_insurance.html')

def visa_assistance(request):
    return render(request, 'visa_assistance.html')

def customer_support(request):
    return render(request,"customer.html")

def paris(request):
    return render(request,"Paris.html")

def rome(request):
    return render(request,"rome.html")

def bali(request):
    return render(request,"bali.html")

def capetown(request):
    return render(request,"capetown.html")

def newyork(request):
    return render(request,"newyork.html")

def sydney(request):
    return render(request,"sydney.html")

def tokyo(request):
    return render(request,"tokyo.html")

def dubai(request):
    return render(request,"dubai.html")


def book(request):
    destination = request.GET.get('destination', 'Unknown')
    return render(request, 'booking.html', {'destination': destination})

def effiel(requrst):
    return render(requrst, 'effiel.html')

def louvre(requrst):
    return render(requrst, 'louvre.html')


def login(request):
    return render(request,"login.html")

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)




from django.shortcuts import render

def payment_page(request):
    return render(request, 'payment.html')



from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from .utils import save_user_to_excel, get_user_data_from_excel, save_user_profile_to_excel

# Signup view
def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Save user to Excel (email, phone, password)
        if save_user_to_excel(email, phone, password):
            request.session['email'] = email  # Save email to session after successful signup
            return redirect('profile')  # Redirect to profile for additional details
        else:
            return JsonResponse({"message": "Error saving user data."}, status=500)

    return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("emailOrPhone")
        password = request.POST.get("password")

        # Check user credentials in Excel
        user_data = get_user_data_from_excel(email)
        if user_data and user_data['password'] == password:
            request.session['email'] = email  # Save email to session
            return redirect('profile')  # Redirect to profile page if login is successful
        else:
            return render(request, 'login.html', {"error": "Invalid email or password."})

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile view
def profile(request):
    email = request.session.get('email')
    user_data = get_user_data_from_excel(email)

    if user_data:
        # If user has data in the profile, show it; else, prompt for profile creation
        return render(request, 'profile.html', {'user': user_data})
    else:
        return redirect('login')

# Update profile view
def update_profile(request):
    if request.method == 'POST':
        email = request.session.get('email')
        name = request.POST.get('name')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        preferences = request.POST.get('preferences')
        budget = request.POST.get('budget')
        linkedin = request.POST.get('linkedin')
        instagram = request.POST.get('instagram')
        travel_history = request.POST.get('travel_history')

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            profile_picture_url = fs.url(filename)
        else:
            profile_picture_url = None

        # Save the profile information in the Excel file
        if save_user_profile_to_excel(email, name, address, dob, gender, preferences, budget, linkedin, instagram, travel_history, profile_picture_url):
            return JsonResponse({"message": "Profile updated successfully!"}, status=200)
        else:
            return JsonResponse({"message": "Error updating profile."}, status=500)

    return redirect('profile')



from django.http import JsonResponse
from .utils import save_contact_to_excel
from django.shortcuts import render

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        success = save_contact_to_excel(name, email, message)
        if success:
            return JsonResponse({"message": "Message sent successfully!"}, status=201)
        else:
            return JsonResponse({"message": "Error saving user data."}, status=500)
    
    return render(request, "Contact.html")


def explore_destinations(request):
    return render(request, 'explore_destinations.html')

import os
import openpyxl
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from travel_app.weather import send_weather_email

def submit_booking(request):
    if request.method == 'POST':
        # Extract booking details
        name = request.POST.get('name')
        email = request.POST.get('email')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        guests = request.POST.get('guests')
        notes = request.POST.get('notes')

        # Save booking to Excel
        booking_saved = save_booking_to_excel(name, email, destination, date, guests, notes)
        if not booking_saved:
            return HttpResponse("Failed to save booking. Please try again.")

        # Generate ticket PDF
        ticket_path = generate_ticket_pdf(name, destination, date, guests, notes)
        if not ticket_path:
            return HttpResponse("Error generating the ticket. Please try again later.")

        # Send ticket via email
        email_sent = send_ticket_email(email, name, ticket_path)
        if not email_sent:
            return HttpResponse("Booking saved, but failed to send email.")
        
         # ✅ Send immediate weather email at booking time
        send_weather_email(email, destination,date)

        # ✅ Schedule daily weather updates until trip date
        schedule_daily_weather_emails(email, destination, date)

        return HttpResponse(f"Thank you, {name}! Your trip to {destination} has been booked. Check your email for the ticket.")
    
    return HttpResponse("Invalid request.")
from datetime import datetime, timedelta
from sib_api_v3_sdk import TransactionalEmailsApi, ApiClient, Configuration
from django.http import HttpResponse
from travel_app.weather import send_weather_email
from travel_app.utils import get_weather_forecast
def schedule_daily_weather_emails(email, destination, trip_date):
    """Schedules a daily weather email until the trip date"""
    today = datetime.today().date()
    trip_date = datetime.strptime(trip_date, '%Y-%m-%d').date()
    
    # Send a weather report daily until the trip date
    while today <= trip_date:
        weather_details = get_weather_forecast(destination, today)
        send_weather_email(email, destination, weather_details)
        today += timedelta(days=1)  # Move to the next day
        
from openpyxl import Workbook
import tempfile
from datetime import datetime

import os
from openpyxl import Workbook
from datetime import datetime

import os
from openpyxl import Workbook, load_workbook
from datetime import datetime

def save_booking_to_excel(name, email, destination, date, guests, notes):
    try:
        # Define the path where the Excel file will be saved
        excel_path = 'travel_app/storage/bookings.xlsx'

        # Check if the file exists
        if os.path.exists(excel_path):
            # Load the existing workbook
            wb = load_workbook(excel_path)
            ws = wb.active
        else:
            # Create a new workbook if the file doesn't exist
            wb = Workbook()
            ws = wb.active
            # Add headers if creating a new file
            ws.append(['Name', 'Email', 'Destination', 'Travel Date', 'Guests', 'Notes', 'Booking Date'])

        # Append booking details with the current timestamp
        ws.append([name, email, destination, date, guests, notes, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

        # Save the workbook with the updated data
        wb.save(excel_path)

        print(f"Booking saved to Excel file: {excel_path}")
        return True
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return False


def generate_ticket_pdf(name, destination, date, guests, notes):
    try:
        template = get_template('ticket_template.html')
        context = {'name': name, 'destination': destination, 'date': date, 'guests': guests, 'notes': notes}
        html = template.render(context)
        ticket_path = os.path.join(settings.MEDIA_ROOT, f"{name}_ticket.pdf")
        with open(ticket_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            raise Exception("PDF generation failed")
        return ticket_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

import os
from django.conf import settings


import os
from django.conf import settings

def send_ticket_email(email, name, ticket_path):
    try:
        subject = "Your Trip Booking Confirmation"
        body = f"Hi {name},\n\nThank you for booking your trip with us! Please find your ticket attached."

        email_message = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [email],
        )

        # Attach the ticket file if it exists
        if os.path.exists(ticket_path):
            email_message.attach_file(ticket_path)

        # Send the email with fail_silently=False for debugging
        email_message.send(fail_silently=False)

        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False




def test_file_write(request):
    try:
        test_file_path = os.path.join(settings.MEDIA_ROOT, 'test.txt')
        with open(test_file_path, 'w') as f:
            f.write('test')
        return HttpResponse("File write successful")
    except Exception as e:
        return HttpResponse(f"Error writing file: {e}")
    
import json
import os
import difflib
from django.shortcuts import render
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Initialize chatbot
chatbot = ChatBot('TravelBot')

# Define the exact path to the training data JSON file
DATA_FILE = r"C:\travel_agency\travel_agency\travel_app\storage\training_data.json"

# Load training data from JSON file
def load_training_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

# Load training data
training_data = load_training_data()

# Train the chatbot
trainer = ListTrainer(chatbot)
for question, answer in training_data.items():
    trainer.train([question, answer])

# Function to find the best-matching question
def get_best_match(user_input):
    user_input = user_input.lower().strip()  # Convert input to lowercase & remove extra spaces
    questions = [q.lower().strip() for q in training_data.keys()]  # Normalize stored questions

    # First try fuzzy matching with a lower cutoff for more flexibility
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.4)

    if matches:
        best_match = matches[0]
        for key in training_data.keys():
            if key.lower().strip() == best_match:
                return training_data[key]  # Return the correct answer

    # Check for exact match as fallback
    if user_input in questions:
        return training_data[user_input]

    # Fallback response if no match is found
    return "I'm sorry, I don't understand that. Can you ask differently or check our website for more info?"

# Chatbot response function
def chat_response(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "").strip()
        print(f"User input: {user_input}")  # Debugging statement to see the input
        bot_response = get_best_match(user_input)  # Use fuzzy matching for response
        print(f"Bot response: {bot_response}")  # Debugging statement to see the response
        return JsonResponse({"response": bot_response})

    return JsonResponse({"response": "Invalid request."})

import requests
from sib_api_v3_sdk import TransactionalEmailsApi, ApiClient, Configuration
from sib_api_v3_sdk.rest import ApiException

def get_weather(city):
    # Get your API key from OpenWeatherMap (or other weather API provider)
    weather_api_key = '745187ba5752d4c0e9be45a51441b8ea'
    
    # URL to get the weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        
        # If the response is successful
        if data.get('cod') == 200:
            temp = data['main']['temp']
            weather_desc = data['weather'][0]['description']
            return f"The current temperature in {city} is {temp}°C with {weather_desc}."
        else:
            return f"Could not retrieve weather information for {city}."
    except Exception as e:
        return f"An error occurred while fetching weather data: {e}"

def send_email_via_sendinblue(to_email, subject, content):
    # Set your Sendinblue API key here
    api_key = 'Sendinblue Key'  # Replace with your actual API key

    # Configure the API client with your API key
    configuration = Configuration()
    configuration.api_key['api-key'] = api_key

    # Initialize the API instance
    api_instance = TransactionalEmailsApi(ApiClient(configuration))

    # Define the sender and recipient
    sender = {"email": "rahulgupta160602@gmail.com"}
    recipient = [{"email": to_email}]

    # Define the email content
    html_content = content

    # Create the email data
    send_smtp_email = {
        "sender": sender,
        "to": recipient,
        "subject": subject,
        "htmlContent": html_content
    }

    # Send the email
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully: {api_response}")
    except ApiException as e:
        print(f"Error sending email: {e}")

def send_weather_email(to_email, city):
    # Get the weather information
    weather_details = get_weather(city)
    
    # Send the email with the weather details
    send_email_via_sendinblue(to_email, f"Weather Update for {city}", weather_details)

from django.http import HttpResponse
from travel_app.weather import send_weather_email  # Import the function from the file where it's written

def send_weather(request):
    # This will send the weather email
    send_weather_email("kumarr47872@gmail.com", "London")
    
    # You can return a simple response confirming the email is sent
    return HttpResponse("Weather email sent successfully!")
