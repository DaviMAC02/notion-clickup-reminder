import json
import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Initialize the Telegram bot using your bot token
bot = telegram.Bot(token='6297703034:AAHpAtl7LxrNZyBWHREoxVbTNkYyRdkXT7A')

# Set the chat ID that the bot will listen to
chat_id = '-846111004'

affirmative_responses = ['yes', 'y', 'sim', 's', 'ok', 'okay', 'certo', 'claro', 'affirmative', 'affirmativo', 'positivo']

# Define the function to handle user messages
def handle_message(update, context):
    message = update.message.text
    user_id = update.message.from_user.id
    print(f"Received message '{message}' from user {user_id}")
    if message.lower() in affirmative_responses:
        # Load the user_responded JSON file and update the flag
        with open('user_responded.json', 'r') as f:
            print("Updating user_responded.json")
            user_responded = json.load(f)
            user_responded["user_responded"] = True
        # Save the updated JSON file
        with open('user_responded.json', 'w') as f:
            json.dump(user_responded, f)
        # Send a message to the user
        bot.send_message(chat_id=chat_id, text="Perfeito, bom trabalho e bom descanso")

# Set up the Telegram updater and dispatcher
updater = Updater(token='6297703034:AAHpAtl7LxrNZyBWHREoxVbTNkYyRdkXT7A', use_context=True)
dispatcher = updater.dispatcher

# Set up the message handler to respond to user messages
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
dispatcher.add_handler(message_handler)

print("Starting bot...")

# Start the Telegram bot and handle CTRL+C
try:
    updater.start_polling()
    print("Bot started")
    updater.idle()
except KeyboardInterrupt:
    updater.stop()