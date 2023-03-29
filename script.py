import json
import pytz
import telegram
import time
from datetime import datetime, timezone, time as dtime
import asyncio

from typing import List, Dict, Any, Union


class TelegramBot:
    def __init__(self, token: str, chat_id: str):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    async def send_message(self, message: str):
        await self.bot.send_message(chat_id=self.chat_id, text=message)


class NotionReminder:
    def __init__(self, user_name: str, start_time: dtime, end_time: dtime, days_of_week: List[str], reminder_interval: int, timezone_name: str):
        self.user_name = user_name
        self.start_time = start_time
        self.end_time = end_time
        self.days_of_week = days_of_week
        self.reminder_interval = reminder_interval
        self.timezone = pytz.timezone(timezone_name)

    def _is_weekday_within_time_period(self, now: datetime) -> bool:
        return (now.strftime('%A') in self.days_of_week) and (self.start_time <= now.time() <= self.end_time)

    async def remind(self, bot: TelegramBot):
        while True:
            now = datetime.now(timezone.utc).astimezone(self.timezone)
            print(f'Today is {now.strftime("%A")} and the time is {now.strftime("%H:%M")}, checking if it is time to send a reminder...')
            if self._is_weekday_within_time_period(now):
                print("Reminder period started")
                with open('user_responded.json', 'r') as f:
                    user_responded = (json.load(f))['user_responded']
                if not user_responded:
                    while self.start_time <= datetime.now(self.timezone).time() <= self.end_time and not user_responded:
                        bot.send_message(f"Olá {self.user_name}, passando para te lembrar de preencher o seu Notion!")
                        now = datetime.now(self.timezone)
                        if now.time() >= self.end_time:
                            break
                        await asyncio.sleep(self.reminder_interval)
                        with open('user_responded.json', 'r') as f:
                            user_responded = (json.load(f))['user_responded']
                with open('user_responded.json', 'r') as f:
                    user_responded = json.load(f)['user_responded']
                if user_responded:
                    with open('user_responded.json', 'w') as f:
                        json.dump({"user_responded": False}, f)
                print("Sleeping until tomorrow")
                await asyncio.sleep((datetime.combine(now.date(), self.end_time) - now).seconds)

async def main():
    bot = TelegramBot(token='6297703034:AAHpAtl7LxrNZyBWHREoxVbTNkYyRdkXT7A', chat_id='-846111004')
    reminder = NotionReminder(user_name='Davi',
                              start_time=dtime(hour=20, minute=0),
                              end_time=dtime(hour=23, minute=0),
                              days_of_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                              reminder_interval=3600,
                              timezone_name='America/Sao_Paulo')
    await reminder.remind(bot)

if __name__ == "__main__":
    asyncio.run(main())
