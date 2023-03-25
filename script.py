import json
import pytz
import telegram
import time
from datetime import datetime


# Initialize the Telegram bot using your bot token
bot = telegram.Bot(token='6297703034:AAHpAtl7LxrNZyBWHREoxVbTNkYyRdkXT7A')

# Set the chat ID that the bot will send messages to
chat_id = '-940741368'

# Define user name
user_name = "Davi"

# Define the message to be sent
message = f"Olá {user_name}, passando para te lembrar de preencher o seu Notion!" 

# Define the start and end times of the reminder period
start_time = datetime.strptime('17:00', '%H:%M').time()
end_time = datetime.strptime('20:00', '%H:%M').time()

# Define the days of the week on which to send the reminder
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Define the interval between reminders in seconds
reminder_interval = 5 # 1 hour


while True:
    # Get the current datetime in UTC timezone
    utc_now = datetime.utcnow()

    # Convert the UTC datetime to UTC-3 timezone
    utc_3 = pytz.timezone('UTC-3')
    now = utc_3.localize(utc_now)
    print(f'Today is {now.strftime("%A")} and the time is {datetime.now().strftime("%H:%M")}, checking if it is time to send a reminder...')

    # Check if it is a weekday and within the reminder period
    if now.strftime('%A') in days_of_week and start_time <= now.time() <= end_time:
        print("Reminder period started")
        # Retrieves the user_responded flag from the JSON file
        with open('user_responded.json', 'r') as f:
            user_responded = (json.load(f))['user_responded']
                
        # If the user has not responded, send reminders every hour
        if user_responded == False:
            while start_time <= datetime.now().time() <= end_time and user_responded == False:
                bot.send_message(chat_id=chat_id, text=message)
                now = datetime.now()
                if now.time() >= end_time:
                    break
                time.sleep(reminder_interval)
                # Retrieves the user_responded flag from the JSON file
                with open('user_responded.json', 'r') as f:
                    user_responded = (json.load(f))['user_responded']
        
        # Reset the flag for the next day
        if user_responded == True:
            with open('user_responded.json', 'r') as f:
                user_responded = json.load(f)
                user_responded["user_responded"] = False
            # Save the updated JSON file
            with open('user_responded.json', 'w') as f:
                json.dump(user_responded, f)
      # Sleep the exact time remaining until the next day
        print("Sleeping until tomorrow")
        time.sleep((datetime.combine(now.date(), end_time) - now).seconds)
                
      
