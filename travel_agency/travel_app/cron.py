from django_cron import CronJobBase, Schedule
from datetime import datetime
from travel_app.weather import send_weather_email
from travel_app.utils import get_booking_data

class SendDailyWeatherEmails(CronJobBase):
    RUN_EVERY_MINS = 1440  # 24 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'travel_app.send_daily_weather_emails'

    def do(self):
        bookings = get_booking_data()
        today = datetime.today().strftime('%Y-%m-%d')

        for booking in bookings:
            if booking['TripDate'] >= today:  # Only send for future trips
                send_weather_email(booking['Email'], booking['Destination'])
